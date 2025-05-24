import httpx

async def get_coordinates(city: str):
    url = "https://nominatim.openstreetmap.org/search "
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers)
        data = resp.json()
        if data and isinstance(data, list) and len(data) > 0:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            raise ValueError(f"City '{city}' not found")