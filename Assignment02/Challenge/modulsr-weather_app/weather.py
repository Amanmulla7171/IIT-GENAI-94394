# weather.py

import requests

api_key = "3c557e82e2dff710aa821313a49b1dfd"


def get_weather_info(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid city or API error"}

    data = response.json()

    # Extract important details
    important_info = {
        "City": data.get("name"),
        "Temperature (°C)": data["main"].get("temp"),
        "Feels Like (°C)": data["main"].get("feels_like"),
        "Humidity (%)": data["main"].get("humidity"),
        "Pressure (hPa)": data["main"].get("pressure"),
        "Weather": data["weather"][0].get("description"),
        "Wind Speed (m/s)": data["wind"].get("speed"),
    }

    return important_info
