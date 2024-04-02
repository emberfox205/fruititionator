# fruititionator
![Static Badge](https://img.shields.io/badge/Python-3.8.5-blue?style=flat&logo=Python&logoColor=white)

A Python project to detect fruits using Computer Vision and return their nutrition values.

## Documentation
#### API call 
- All necessary functions are in `API_call.py`.
- The script takes one string argument `keyword`, which is then used to query USDA Central Food Database (specifically the Foundation Food and SR Legacy) using the `get_api()` function. It returns a dictionary of information about the ONE most relevant result.
- Shortened example of the return value of `get_api()`:
```Python
{
    "fdcId": 1750339,
    "description": "Apples, red delicious, with skin, raw",
    "dataType": "Foundation",
    "publicationDate": "2020-10-30",
    "ndbNumber": "9500",
    "foodNutrients": [
        {
            "number": "303",
            "name": "Iron, Fe",
            "amount": 0.0,
            "unitName": "MG",
            "derivationCode": "A",
            "derivationDescription": "Analytical"
        },
        {
            "number": "304",
            "name": "Magnesium, Mg",
            "amount": 4.7,
            "unitName": "MG",
            "derivationCode": "A",
            "derivationDescription": "Analytical"
        }
    ]
}
```
- To only get the dictionary of relevant data (name, amount, unit), use the `format_data()` function with the very return value of `get_api()` as the argument. `format_data()` returns a dictionary of nutrients, with key being the **name** and value being a list containing **amount** and **unit**.
- Shortened example of the return value of `format_data()`:
```Python
{
    "Magnesium, Mg": [
        4.7,
        "MG"
    ],
    "Phosphorus, P": [
        9.18,
        "MG"
    ],
    "Potassium, K": [
        95.3,
        "MG"
    ]
}
```
> [!NOTE]
> Remember to have `.env` file in the same directory as `API_call.py`, and **DO NOT** share the API key.


