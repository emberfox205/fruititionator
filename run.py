from Fruit_Detectors import detect_fruit
from API_call import get_api, format_data
import json

def usage():
    fruit_name = detect_fruit()[0]
    response = get_api(fruit_name)
    print(f"{response['description']}: {response['fdcId']}")
    if response:
        print(json.dumps(format_data(response), indent=4))
    else:
        print(response)

usage()
    