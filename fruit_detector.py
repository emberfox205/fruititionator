# Responsible for scanning fruit objects.

import time
import cv2
import numpy as np
from keras.models import load_model
from custom_classes import Detected_Object


def detect_fruit(client, DETECTED_OBJ_FEED_ID, CONFIDENCE_FEED_ID) -> Detected_Object:
    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    with open("labels.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]

    # Initialize camera
    camera = cv2.VideoCapture(0)

    detected_fruits = []
    frame_thres = 0
    last_class = None

    while True:
        image = camera.read()[1]

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

        # publish every 30th frame
        client.publish(CONFIDENCE_FEED_ID, str(np.round(confidence_score * 100)))

        if frame_thres % 30 == 0 and last_class == class_name[2:]:
            client.publish(DETECTED_OBJ_FEED_ID, class_name[2:])
        elif last_class != class_name[2:]:
            client.publish(DETECTED_OBJ_FEED_ID, class_name[2:])

        time.sleep(1.5)
        last_class = class_name[2:]
        frame_thres += 1

        detected_fruits.append({
            "fruit_name": class_name[2:],
            "confidence_score": float(np.round(confidence_score * 100)),
            "image": cv2.cvtColor(((image[0] + 1) * 127.5), cv2.COLOR_BGR2RGB).astype(np.uint8)  # Save the image for display
        })

        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            max_score, index = 0, 0
            last_result = detected_fruits[-5:]

            for i in last_result:
                if i["confidence_score"] > max_score:
                    max_score = i["confidence_score"]
                    index = i

            last_detection = last_result[last_result.index(index)]
            detected_obj = Detected_Object(last_detection["fruit_name"],
                                           last_detection["confidence_score"],
                                           last_detection["image"])
            print(detected_obj, f"frame: {frame_thres}")
            camera.release()
            cv2.destroyAllWindows()
            return detected_obj

        frame_thres += 1
