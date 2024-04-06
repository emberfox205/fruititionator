from Fruit_Detectors import detect_fruit
from API_call import get_api
import time

def get_nutrition():
    detected_fruit = detect_fruit()
    return get_api(detected_fruit.name)

def main():
    scan_count = 0
    fruits_detected = []
    while True:
        fruit_nutrition = get_nutrition()
        if fruit_nutrition.nutrition == {}:
            print("Unable to get data value, closing...")    
            break
        else:
            fruits_detected.append(fruit_nutrition.name)
            print(fruit_nutrition)
            prompt = input("input 'e' for rescan, anything else to stop the program: ")
            if prompt == 'e':
                print("__RESTARTING__")
                scan_count += 1
                time.sleep(0.5)
            else:
                print("User timed out")
                print(f"Scan count {scan_count}")
                for fruit in fruits_detected:
                    print(f"Name: {fruit}")
                break
    
if __name__ == '__main__':
    main()
 