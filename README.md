# fruititionator
![Static Badge](https://img.shields.io/badge/Python-3.8.5-blue?style=flat&logo=Python&logoColor=white)

A Python project to detect fruits using Computer Vision and return their nutrition values.

## Documentation
#### CLI client (temporary)
 - Purpose: provides a practical demo to test changes in other files.
 - First detects with `detect_fruit()` and gets the nutrition with `get_api()` using the `Detected_Object.name` attribute as argument. All this is abstracted within the `get_nutrition()` function. The function returns an instance of `Fruit_Nutrition` class.
 - In `main()`, the program either exits upon detecting empty response or prints out the nutrition onto the terminal. Upon finishing with the query, user is asked to either continue or exit using hotkeys (`e` or otherwise).
 - Upon exiting, the program prints number of scans (times used) and a list of detected fruits. 
#### Image Detection 
 - Relevant functions are in `Fruit_Detectors.py`. 
 - The `detect_fruit()` function takes no argument. It opens the device's camera (if available and given permission) and also initiates a window showing the camera feed. The model looks for one out of ten possible classes of objects, one of which being `Nothing` and the rest being types of fruits.
> [!NOTE]
> All the fruit classes' names can be found in `labels.txt`.
 - The function returns an instance of the `Detected_Object` class, which contains 3 attributes:
     - `name` of type `str`.
     - `score` of type `float`.
     - `image` of type `ndarray`. 
#### API call 
- All necessary functions are in `API_call.py`.
- The script takes one string argument `keyword`, which is then used to query USDA Central Food Database (specifically the Foundation Food and SR Legacy) using the `get_api()` function. It returns an instance of the `Fruit_Nutrition` dataclass, which contains 3 attributes:
    -  `name` of type `str`.
    -  `fdcId` of type `int`
    -  `nutrition` of type `dict`. Inside `nutrition`, a key-value pair consists of `nutrient_name` as key, an f-string `f"{amount} {unit}"` as value.
> [!NOTE]
> Info about `Detected_Object` and `Fruit_Nutrition` classes are in `custom_classes.py`.
- In case the keyword is invalid, the function returns `None`.
- Example of printing `Fruit_Nutrition` / the return value of `get_api()`:
```
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


