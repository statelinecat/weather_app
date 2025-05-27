import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
query = "москв"

params = {
    "namePrefix": query,
    "languageCode": "ru",
    "limit": 5,
    "types": "CITY"
}

headers = {
    "X-RapidAPI-Key": "5daecbb569mshbff5b5ffc209c66p1f4e44jsn08ebe8685a46",
    "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.json())
