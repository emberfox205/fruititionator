# fruititionator

![Static Badge](https://img.shields.io/badge/Python-3.8.5-blue?style=flat&logo=Python&logoColor=white)

Fruititionator is a Python project that leverages Computer Vision to detect fruits in real-time, fetch their nutritional values, and publish this data to an Adafruit IO dashboard using MQTT.

## Installation

Clone the repo:

`$ git clone git@github.com:emberfox205/fruititionator.git`

Import libaries (with pip):

`$ pip install -r requirements.txt`

Get your USDA FoodData Central API key [here](https://fdc.nal.usda.gov/api-key-signup.html).

Make an Adafruit IO account [here](https://accounts.adafruit.com/users/sign_up) or log in [here](https://accounts.adafruit.com/users/sign_in).

Click on the key icon on the top right orner of the IO tab to view your Adafruit IO (AIO) username and key.

![Account Page > IO tab > Gold-Circle-with-Black-Key logo](https://cdn.discordapp.com/attachments/1071117548311027723/1236281850297585694/Adafruit_IO_key_scr.png?ex=663770b2&is=66361f32&hm=3f0853b7cca30d170020b3cd271bedf5251de2a85d230dbed278bf45caa0a2fe&)

In your local repo, create a `.env` file:

`$ code .env`

Structure it like this:

```.env
API_KEY=USDA_FDC_key_goes_here
AIO_USERNAME=AIO_username_goes_here
AIO_KEY=AIO_key_goes_here
```

Replace `your_usda_api_key`, `your_aio_username`, and `your_aio_key` with your actual keys.

To track published data on your Adafruit account, create four feeds with the following names and specifications:

1. Confidence Score: Feed History On
2. Detected Object: Feed History On
3. Captured Image: Feed History Off
4. Nutrition Values: Feed History Off

To view them in a compact GUI, create a dashboard, then blocks of the same name as the feeds and connect them to their respective feed.

> [!NOTE] 
> Some values are best displayed on specific block types:
> 
> "Captured Image" -> "Image" block.
> 
> "Nutrition Values" -> "Multiline Text" block.

### Running the Project

After installation, in your local repo, navigate to `mqtt_client.py` and run the project. Alternatively, execute in your terminal the following:

`$ python mqtt_client.py`

## Documentation

### MQTT Client

- The client acts as an interface between code files and the dashboard.
- The file is run as normal without specific CLI commands.
- It first detects with `detect_fruit()`. To conclude detection, press `esc` while the video feed is in focus (click on the video feed window to gain focus).
- Nutritional values are fetched and published using the `api_call.py` module, while the image corresponding to the chosen detection result is published using the `image_processor.py` module.
- The program then either prints the data or warns user if nothing is detected. User is prompted to input `e` to continue scanning or any other key to exit.
- Upon exiting, the program prints number of successful scans (instances that a fruit is detected) and a list of detected fruits.

### Image Detection

- Relevant functions are in `fruit_detector.py`.
- The `detect_fruit()` function takes no argument. It opens the device's camera (if available and given permission) and also initiates a window showing the camera feed. The model looks for one out of the possible classes of objects, one of which being `Nothing` and the rest being types of fruits.
- This function is also responsible for publishing to 2 Adafruit feeds: `Confidence Score` and `Detected Object`.

> [!NOTE]
> All the fruit classes' names can be found in `labels.txt`.

- The function returns an instance of the `Detected_Object` class, which contains 3 attributes:
  - `name` of type `str`.
  - `score` of type `float`.
  - `image` of type `ndarray`.

### API call

- All necessary functions are in `api_call.py`.
- The script takes one string argument `keyword`, which is then used to query USDA Central Food Database (specifically the Foundation Food and SR Legacy) using the `get_api()` function. It returns an instance of the `Fruit_Nutrition` dataclass, which contains 3 attributes:
  - `name` of type `str`.
  - `fdcId` of type `int`
  - `nutrition` of type `dict`. Inside `nutrition`, a key-value pair consists of `nutrient_name` as key, an f-string `f"{amount} {unit}"` as value.

> [!NOTE]
> Info about `Detected_Object` and `Fruit_Nutrition` classes are in `custom_classes.py`.

- In case the keyword is invalid, the function returns `None`.
- `api_call.py` also handles the publishing of the nutrition to `Nutrition Values` feed on Adafruit IO.
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
> Remember to have `.env` file in the same directory as `api_call.py`, and **DO NOT** share the API key.

### Image modification and encoding

- Relevant functions are in `image_processor.py`

#### Functions

`resize_image(image, target_size=100)`

- This function takes a numpy array representing an image and a target size in kilobytes, and returns a PIL Image object that is resized such that the size of the encoded image is less than or equal to the target size.

- The function converts the numpy array to a PIL Image object, and then enters a loop where it encodes the image, checks the size of the encoded image, and if the size is greater than the target size, resizes the image by a factor and repeats the process. The loop continues until the size of the encoded image is less than or equal to the target size.

`encode_image(image_pil)`

- This function takes a PIL Image object, encodes it in JPEG format, and then encodes the result in base64. It returns the base64-encoded image as a string.

`image_publisher(client, IMAGE_FEED_ID, ndarray_image)`

- This function takes a MQTT client, an image feed ID, and a numpy array representing an image. It calls resize_image to resize the image, encode_image to encode the resized image, and then publishes the encoded image to the MQTT feed specified by IMAGE_FEED_ID.
