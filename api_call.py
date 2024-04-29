import json
import os
import requests
from dotenv import load_dotenv
from typing import Union
from custom_classes import Fruit_Nutrition

load_dotenv()
API_KEY = os.getenv('API_KEY')


# Request and receive nutrition data
def get_api(client, NUTRITION_FEED_ID, keyword: str) -> Union[Fruit_Nutrition, None]:
    url = "https://api.nal.usda.gov/fdc/v1/foods/list"
    data = {
        "generalSearchInput": keyword,
        "dataType": ["Foundation", "SR Legacy"],
        "requireAllWords": True,
        "foodCategory": "Fruits and Fruit Juices",
        "sortBy": "score",
        "sortOrder": "desc"
    }

    response = requests.post(url, json=data, params={"api_key": API_KEY})
    
    # Print the status code of the response
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        res_json: list = list(response.json())
        if res_json:
            # Format and return the received data
            return format_data(client, NUTRITION_FEED_ID, res_json[0], keyword)  
        else:
            # Publish "None" to the nutrition feed if no data is found
            client.publish(NUTRITION_FEED_ID, "None") 
            return None
    else:
        return None
    
# Format the received data for the CLI and Adafruit IO dashboard    
def format_data(client, NUTRITION_FEED_ID, response: list, fruit_name: str) -> Fruit_Nutrition:
    nutrition = {}
    for nutrient in response["foodNutrients"]:
        name = nutrient["name"]
        unit = nutrient["unitName"]
        amount = nutrient["amount"]
        if amount > 0 and unit != "kJ":
            if name not in nutrition.keys():
                nutrition[name] = f"{amount} {unit}"
    
    # Create a Fruit_Nutrition object with the formatted data
    fruit_nutrition = Fruit_Nutrition(fruit_name, response["fdcId"], nutrition)
    
    # Convert the nutrition data to JSON format
    nutrition_json = json.dumps(nutrition, indent=2)
    
    # Publish the nutrition data to the NUTRITION_FEED_ID
    client.publish(NUTRITION_FEED_ID, nutrition_json)
    
    return fruit_nutrition
