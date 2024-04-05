class fruit_data:
    def __init__(self, id: int, name: str, nutrition: dict) -> dict:
        self.name = name
        self.nutrition = nutrition
        self.fid = id
    def data_dict(self):
        return {self.name: self.nutrition}
    def __str__(self):
        return f"ID: {self.fid}: {self.name}"