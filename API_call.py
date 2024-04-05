import requests, os, json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_api(keyword: str) -> dict:
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
        return res_json[0] if res_json else {}
    else:
        return {}
    
def format_data(response: list) -> dict:
    nutrition_data = {}
    for nutrient in response["foodNutrients"]:
        name = nutrient["name"]
        unit = nutrient["unitName"]
        amount = nutrient["amount"]
        if amount > 0 and unit != "kJ":
            if name not in nutrition_data.keys():
                nutrition_data[name] = [amount, unit]
    return nutrition_data

def main():
<<<<<<< HEAD
    keyword = "con cu"
=======
    keyword = "HMS Hood"
>>>>>>> main
    response = get_api(keyword)  
    if response:
        print(f"{response['description']}: {response['fdcId']}")
        print(json.dumps(format_data(response), indent=4))
    else:
        print(response)
        
if __name__ == "__main__":
    main()
    
