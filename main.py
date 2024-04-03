import json
import cv2
import numpy as np
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from Fruit_Detectors import detect_fruit

class FruitDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Detection")

        self.label = Label(root, text="", font=("Arial", 16))

        self.label.pack()

            
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack(pady=20)
        
        self.scan_button = tk.Button(root, text="Scan", command=self.detect_fruit)
        self.scan_button.pack(pady=20)

    def detect_fruit(self):

        detected_fruits = detect_fruit()
        last_detection = detected_fruits[-1]
        
        self.label.config(text=f"Detected Fruit: {last_detection['fruit_name']}")
        self.label.config(text=f"Confidence Score: {last_detection['confidence_score']}")
        self.display_image(last_detection['image'])

    def display_image(self, image):
        """Display image in a tkinter window."""
        if image is None:
            print("Error: Unable to capture image from camera.")
            return

        image = Image.fromarray((image*255).astype(np.uint8)).resize((244, 244)).convert('RGB')
        image = ImageTk.PhotoImage(image=image)
        
        if hasattr(self, 'image_on_canvas'):
            self.canvas.delete(self.image_on_canvas)
        
        self.image_on_canvas = self.canvas.create_image(20, 100, anchor=tk.NW, image=image)
        self.canvas.image = image


if __name__ == "__main__":
    root = tk.Tk()
    app = FruitDetectorApp(root)
    root.mainloop()
