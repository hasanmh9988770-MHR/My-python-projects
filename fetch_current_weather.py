import requests

# 1. Setup
api_key = "866d8cb601cdfc1a8117e8f70d9e3ded"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# 2. Input
city_name = input("Enter city name: ")

# 3. URL Construction (Added units=metric for Celsius)
complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"

try:
    response = requests.get(complete_url)
    data = response.json()

    # 4. Modern Python 3.10+ Pattern Matching
    match data.get("cod"):
        case 200:
            main = data["main"]
            weather = data["weather"][0]
            temp = main["temp"]
            desc = weather["description"]

            print(f"\n✅ Success!")
            print(f"🌍 Weather in {city_name.capitalize()}:")
            print(f"🌡️  Temperature: {temp}°C")
            print(f"☁️  Sky: {desc.capitalize()}")

            # --- ADD SMART SUGGESTIONS HERE ---
            print("\n💡 Suggestion:")

            # Check for rain or clouds
            if "rain" in desc.lower():
                print("☔ Grab an umbrella before you head out!")
            elif "cloud" in desc.lower() or "overcast" in desc.lower():
                print("🌥️  It's a bit gloomy, but no umbrella needed yet.")

            # Check for heat
            if temp > 30:
                print("🔥 It's very hot! Stay hydrated and try to stay in the shade.")
            elif temp < 15:
                print("🧣 It's chilly, better wear a jacket.")
            else:
                print("✨ The temperature is quite pleasant.")
            # ----------------------------------

        case 401:
            print("❌ Invalid API Key.")
        case 401:
            print("❌ Invalid API Key. Please check your OpenWeather account.")

        case 404:
            print("❌ City not found. Check the spelling and try again.")

        case _:
            print(f"⚠️ Something went wrong. Error code: {data.get('cod')}")

except Exception as e:
    print(f"🔌 Connection Error: Make sure you are connected to the internet. ({e})")