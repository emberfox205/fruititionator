import os
import sys
import time
from Adafruit_IO import  MQTTClient 
from dotenv import load_dotenv
from api_call import get_api
from fruit_detector import detect_fruit
from image_processor import image_publisher


load_dotenv()
AIO_USERNAME = os.getenv('AIO_USERNAME')
AIO_KEY = os.getenv('AIO_KEY')
CONFIDENCE_FEED_ID = "confidence-score"
DETECTED_OBJ_FEED_ID = "detected-obj"
NUTRITION_FEED_ID = "nutrition-values"
IMAGE_FEED_ID = "captured-image"

def  connected(client):
    print("Connected to the AIO server!!!!")

def  disconnected(client):
    print("Disconnected from the AIO server!!!")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Received: " + payload)
    
client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

def main():
    scan_count = 0
    fruits_detected = []
    while True:
        detected_fruit = detect_fruit(client, DETECTED_OBJ_FEED_ID, CONFIDENCE_FEED_ID)
        time.sleep(0.5)
        image_publisher(client, IMAGE_FEED_ID, detected_fruit.image)
        fruit_nutrition = get_api(client, NUTRITION_FEED_ID, detected_fruit.name)
        if fruit_nutrition == None:
            print("WARNING :: Unable to get data.")    
        else:
            scan_count += 1
            fruits_detected.append(fruit_nutrition.name)
        print(fruit_nutrition)
        prompt = input("INFO :: Input 'e' for rescan, anything else to stop the program: ")
        if prompt == 'e':
            print("__RESTARTING__")
            time.sleep(0.5)
        else:
            client.disconnect()
            time.sleep(0.01)
            print("INFO :: User timed out.")
            print(f"Successful scan count: {scan_count}")
            for fruit in fruits_detected:
                print(f"Name: {fruit}")
            break
    
if __name__ == '__main__':
    client.connect()
    client.loop_background()
    main()
 