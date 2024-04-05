from Fruit_Detectors import detect_fruit
from API_call import get_api, format_data
import json, time
from fruit_shelf import fruit_data

def usage():
    fruit_name = detect_fruit()[0]
    response = get_api(fruit_name)
    if response:
        print(f"{response['description']}: {response['fdcId']}")
        print(json.dumps(format_data(response), indent=4))
        return (json.dumps(format_data(response), indent=4), fruit_name)
    else:
        return response, fruit_name
    
fruit_id = 0
fruits_detected = []
while True:
     nut, name = usage()
     if nut == {}:
        print("Unable to get data value, closing...")    
        break
     else:
        fruit_obj = fruit_data(fruit_id, name, nut)
        fruits_detected.append(fruit_obj)
        try:
            prompt = input("input 'e' for rescan, control-d to stop the program: ")
        except EOFError:
            break
        else:
            if prompt == 'e':
                print("__RESTARTING__")
                fruit_id += 1
                time.sleep(0.5)
            else:
                print("User timed out")
                break

if __name__ == '__main__':
    for _ in fruits_detected:
        print(_)
 