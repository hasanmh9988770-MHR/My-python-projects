import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secure API config
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key:
    raise ValueError("❌ API_KEY not found in .env file")

# Input
city_name = input("Enter city name: ")

# Build URL safely
params = {
    "appid": api_key,
    "q": city_name,
    "units": "metric"
}

try:
    response = requests.get(base_url, params=params)
    data = response.json()

    match data.get("cod"):
        case 200:
            main = data["main"]
            weather = data["weather"][0]

            temp = main["temp"]
            desc = weather["description"]

            print("\n✅ Success!")
            print(f"🌍 Weather in {city_name.capitalize()}:")
            print(f"🌡️ Temperature: {temp}°C")
            print(f"☁️ Sky: {desc.capitalize()}")

            print("\n💡 Suggestion:")

            if "rain" in desc.lower():
                print("☔ Grab an umbrella before you head out!")
            elif "cloud" in desc.lower() or "overcast" in desc.lower():
                print("🌥️ It's a bit gloomy, but no umbrella needed yet.")

            if temp > 30:
                print("🔥 It's very hot! Stay hydrated.")
            elif temp < 15:
                print("🧣 It's chilly, wear a jacket.")
            else:
                print("✨ Weather is pleasant.")

        case "401":
            print("❌ Invalid API Key.")
        case "404":
            print("❌ City not found.")
        case _:
            print(f"⚠️ Error: {data.get('cod')}")

except requests.exceptions.RequestException as e:
    print(f"🔌 Network Error: {e}")
except Exception as e:
    print(f"⚠️ Unexpected Error: {e}")
