##This is the function for the fruit scanning,

import cv2
import numpy as np
from PIL import Image, ImageTk
import numpy as np
import time
from custom_classes import Detected_Object

from keras.models import load_model

def detect_fruit() -> Detected_Object:
    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    with open("labels.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]

    # Initialize camera
    camera = cv2.VideoCapture(0)

    # Initialize start time
    start_time = time.time()

    detected_fruits = []

    while True:
        ret, image = camera.read()

        if image is None:
            print("Error: Unable to capture image from camera.")
            break

        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        cv2.imshow("Webcam Image", image)

        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1

        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        print(f"Class: {class_name[2:]}, Confidence Score: {np.round(confidence_score * 100)}")

        detected_fruits.append({
            "fruit_name": class_name[2:],
            "confidence_score": float(np.round(confidence_score * 100)),
             "image":cv2.cvtColor(((image[0]+ 1) * 127.5), cv2.COLOR_BGR2RGB).astype(np.uint8) # Save the image for display
        })
            
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            last_detection = detected_fruits[-1]
            detected_obj = Detected_Object(last_detection["fruit_name"], last_detection["confidence_score"], last_detection["image"])
            print(detected_fruit)
            camera.release()
            cv2.destroyAllWindows()
            return detected_obj

    

    # Testing the function ouput
if __name__ == '__main__':
    detected_fruit = detect_fruit()
    cv2.imshow("Webcam Image", cv2.cvtColor(detected_fruit.image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()