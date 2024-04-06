# fruititionator
![Static Badge](https://img.shields.io/badge/Python-3.8.5-blue?style=flat&logo=Python&logoColor=white)

A Python project to detect fruits using Computer Vision and return their nutrition values.

## Documentation
#### API call 
- All necessary functions are in `API_call.py`.
- The script takes one string argument `keyword`, which is then used to query USDA Central Food Database (specifically the Foundation Food and SR Legacy) using the `get_api()` function. It returns an instance of the `Fruit_Nutrition` dataclass, which contains attributes `name` of type `str`, `fdcId` of type `int` and `nutrition` of type `dict`. Inside `nutrition`, a key-value pair consists of `nutrient_name` as key, an f-string `f"{amount} {unit}"` as value.
- In case the keyword is invalid, the function returns `None`.
- Example of printing `Fruit_Nutrition` / the return value of `get_api()`:
```
Status code: 200
Fruit Name: apple red delicious
FdcId: 1750339
Nutrition: {
    "Magnesium, Mg": "4.7 MG",
    "Phosphorus, P": "9.18 MG",
    "Potassium, K": "95.3 MG",
    "Zinc, Zn": "0.0196 MG",
    "Copper, Cu": "0.0243 MG",
}
```
> [!NOTE]
> Remember to have `.env` file in the same directory as `API_call.py`, and **DO NOT** share the API key.


