import json
import os
import requests
from dotenv import load_dotenv
from typing import Union
from custom_classes import Fruit_Nutrition


load_dotenv()
API_KEY = os.getenv('API_KEY')

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
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        res_json: list = list(response.json())
        if res_json:
            return format_data(client, NUTRITION_FEED_ID, res_json[0], keyword)  
        else:
            client.publish(NUTRITION_FEED_ID, "None") 
            return None
    else:
        return None
    
def format_data(client, NUTRITION_FEED_ID, response: list, fruit_name: str) -> Fruit_Nutrition:
    nutrition = {}
    for nutrient in response["foodNutrients"]:
        name = nutrient["name"]
        unit = nutrient["unitName"]
        amount = nutrient["amount"]
        if amount > 0 and unit != "kJ":
            if name not in nutrition.keys():
                nutrition[name] = f"{amount} {unit}"
    fruit_nutrition = Fruit_Nutrition(fruit_name, response["fdcId"], nutrition)
    nutrition_json = json.dumps(nutrition, indent=2)
    client.publish(NUTRITION_FEED_ID, nutrition_json)
    return fruit_nutrition

def main():
    keyword = "apple red delicious"
    fruit_data = get_api(keyword)  
    print(fruit_data)
       
if __name__ == "__main__":
    main()
    
