import httpx

import httpx

async def suggest_locations(query: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 5
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyWeatherApp/1.0; +https://example.com)"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers)

        if resp.status_code != 200:
            print("Ошибка запроса:", resp.status_code)
            print("Ответ сервера:", resp.text)
            return []

        try:
            data = resp.json()
        except Exception as e:
            print("Ошибка декодирования JSON:", e)
            print("Сырой ответ:", resp.text)
            return []

        if isinstance(data, list):
            return [item['display_name'] for item in data]
        else:
            return []

