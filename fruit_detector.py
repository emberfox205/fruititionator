import cv2
import numpy as np
from collections import Counter
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

    detected_results = []
    frame = 0
    last_class = None

    while True:
        # Capture image from camera
        image = camera.read()[1]

        if image is None:
            print("Error: Unable to capture image from camera.")
            break

        # Resize image to match model input size
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        cv2.imshow("Webcam Image", image)

        # Preprocess image for model input
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1

        # Make prediction using the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        print(f"Class: {class_name[2:]}, Confidence Score: {np.round(confidence_score * 100)}, Frame: {frame}")

        # Limit publishing rate while keeping the camera feed smooth (about 20 FPS).
        if frame % 30 == 0 and last_class == class_name[2:]:
            client.publish(CONFIDENCE_FEED_ID, str(np.round(confidence_score * 100)))
        if frame % 15 == 0 and last_class != class_name[2:]:
            client.publish(CONFIDENCE_FEED_ID, str(np.round(confidence_score * 100)))
            client.publish(DETECTED_OBJ_FEED_ID, class_name[2:])
            last_class = class_name[2:]
        frame += 1

        # Store detected results
        detected_results.append({
            "fruit_name": class_name[2:],
            "confidence_score": float(np.round(confidence_score * 100)),
            "image": cv2.cvtColor(((image[0] + 1) * 127.5), cv2.COLOR_BGR2RGB).astype(np.uint8)  # Save the image for display
        })

        keyboard_input = cv2.waitKey(1)

        # Once user quits, choose the most common object name, from that choose the result with the highest confidence
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            detected_results = detected_results[-10:]
            freq_counter = Counter([result["fruit_name"] for result in detected_results])
            most_freq_results = [result for result in detected_results if result["fruit_name"] == (freq_counter.most_common(1)[0][0])]
            best_result = max(most_freq_results, key=lambda result: result["confidence_score"])
            detected_obj = Detected_Object(best_result["fruit_name"],
                                           best_result["confidence_score"],
                                           best_result["image"])
            client.publish(CONFIDENCE_FEED_ID, best_result["confidence_score"])
            client.publish(DETECTED_OBJ_FEED_ID, best_result["fruit_name"])

            print(detected_obj)

            # Release camera and close windows
            camera.release()
            cv2.destroyAllWindows()
            return detected_obj
