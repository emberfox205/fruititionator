# fruititionator

![Static Badge](https://img.shields.io/badge/Python-3.8.5-blue?style=flat&logo=Python&logoColor=white)

A Python project to detect fruits using Computer Vision and return their nutrition values.

## Documentation

### MQTT Client

- Purpose: The client acts as an interface between code files and the dashboard.
- The file is run as normal without specific CLI commands.
- First detects with `detect_fruit()` and gets the nutrition with `get_api()` using the `Detected_Object.name` attribute as argument. To conclude detection, press `esc` while the video feed is in focus (click on the video feed window to gain focus).
- The program then either prints the data or warns user if nothing is detected. User is prompted to input `e` to continue scanning or any other key to exit.
- Upon exiting, the program prints number of successful scans (times that a fruit is detected) and a list of detected fruits. 

### Image Detection

- Relevant functions are in `Fruit_Detectors.py`.
- The `detect_fruit()` function takes no argument. It opens the device's camera (if available and given permission) and also initiates a window showing the camera feed. The model looks for one out of ten possible classes of objects, one of which being `Nothing` and the rest being types of fruits.
- This function is also responsible for publishing to 2 Adafruit feeds: `confidence_score` and `detected_obj`.

> [!NOTE]
> All the fruit classes' names can be found in `labels.txt`.
  - The function returns an instance of the `Detected_Object` class, which contains 3 attributes:
  - `name` of type `str`.
  - `score` of type `float`.
  - `image` of type `ndarray`.

### API call

- All necessary functions are in `API_call.py`.
- The script takes one string argument `keyword`, which is then used to query USDA Central Food Database (specifically the Foundation Food and SR Legacy) using the `get_api()` function. It returns an instance of the `Fruit_Nutrition` dataclass, which contains 3 attributes:
  - `name` of type `str`.
  - `fdcId` of type `int`
  - `nutrition` of type `dict`. Inside `nutrition`, a key-value pair consists of `nutrient_name` as key, an f-string `f"{amount} {unit}"` as value.
- `api_call.py` also handles the publishing of the nutrition to `nutrition_values` feed on Adafruit IO. 

> [!NOTE]
> Info about `Detected_Object` and `Fruit_Nutrition` classes are in `custom_classes.py`.

- In case the keyword is invalid, the function returns `None`.
- Example of printing `Fruit_Nutrition` / the return value of `get_api()`:

```bash
Status code: 200
Fruit Name: apple red delicious
FdcId: 1750339
Nutrition: {
    "Magnesium, Mg": "4.7 MG",
    "Phosphorus, P": "9.18 MG",
    "Potassium, K": "95.3 MG",
    "Zinc, Zn": "0.0196 MG",
    "Copper, Cu": "0.0243 MG",
}
```

> [!NOTE]
> Remember to have `.env` file in the same directory as `API_call.py`, and **DO NOT** share the API key.