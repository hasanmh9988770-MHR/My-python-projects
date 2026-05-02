import requests
import time

# Ensure this matches your Flask port (5001)
URL = "http://127.0.0.1:5001/api/generate"

print("🚀 Quote Bot Started... Posting every 10 seconds!")

while True:
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Posted: {data['quote']}")
        else:
            print(f"⚠️ Server returned error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Failed: Is app.py running on 5001?")

    time.sleep(5)  # Wait 10 seconds before posting again