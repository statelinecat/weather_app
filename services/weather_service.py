import httpx

async def get_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast "
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "current_weather": True
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        return resp.json()