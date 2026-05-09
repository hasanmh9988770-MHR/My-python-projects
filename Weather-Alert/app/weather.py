import requests
from flask import current_app

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": current_app.config["WEATHER_API_KEY"],
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=10)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        print("Weather API error:", e)
        return None