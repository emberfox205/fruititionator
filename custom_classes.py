import json

class Detected_Object:
    def __init__(self, name: str, confidence_score: float, image):
        self.name = name
        self.score = confidence_score
        self.image = image 
    def __str__(self):
        return f"Fruit Name: {self.name}\nConfidence Score: {self.score}"

class Fruit_Nutrition:
    def __init__(self, name: str, fdcId: int, nutrition: dict) -> None:
        self.name = name
        self.fdcId = fdcId
        self.nutrition = nutrition
    def __str__(self):
        formatted_nutrition = json.dumps(self.nutrition, indent=4)
        return f"Fruit Name: {self.name}\nFdcId: {self.fdcId}\nNutrition: {formatted_nutrition}"