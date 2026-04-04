import os
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dotenv import load_dotenv
import folium
import webview

# -------------------------
# LOAD API KEY
# -------------------------
load_dotenv()
API_KEY = os.getenv("LOCATION_IQ_TOKEN")
BASE_URL = "https://us1.locationiq.com/v1/search.php"

if not API_KEY:
    raise ValueError("Missing LOCATION_IQ_TOKEN in .env")


# -------------------------
# CACHE
# -------------------------
cache = {}


# -------------------------
# GET LOCATION
# -------------------------
def get_location(address):
    address = address.strip().lower()

    if not address:
        return None

    if address in cache:
        return cache[address]

    try:
        res = requests.get(BASE_URL, params={
            "key": API_KEY,
            "q": address,
            "format": "json"
        }, timeout=10)

        res.raise_for_status()
        data = res.json()

        if not data:
            return None

        top = data[0]

        result = {
            "name": top["display_name"],
            "lat": float(top["lat"]),
            "lon": float(top["lon"])
        }

        cache[address] = result
        return result

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None


# -------------------------
# CREATE MAP
# -------------------------
def create_map(lat, lon, name):
    m = folium.Map(location=[lat, lon], zoom_start=15)

    folium.Marker(
        [lat, lon],
        popup=name,
        tooltip="Location"
    ).add_to(m)

    file_path = os.path.abspath("map.html")
    m.save(file_path)

    return file_path


# -------------------------
# OPEN MAP WINDOW
# -------------------------
def open_map(file_path):
    webview.create_window(
        "🌍 Map View",
        file_path,
        width=900,
        height=600
    )
    webview.start()


# -------------------------
# SEARCH FUNCTION
# -------------------------
def search():
    address = entry.get().strip()

    if not address:
        messagebox.showwarning("Input Error", "Enter address")
        return

    result = get_location(address)

    if not result:
        messagebox.showinfo("Not Found", "No location found")
        return

    lat = result["lat"]
    lon = result["lon"]
    name = result["name"]

    result_label.config(text=f"{name}\nLat: {lat} | Lon: {lon}")

    file = create_map(lat, lon, name)
    open_map(file)


# -------------------------
# GUI SETUP
# -------------------------
app = tk.Tk()
app.title("GeoLocator Pro FIXED")
app.geometry("520x320")
app.configure(bg="#111111")


# STYLE SYSTEM (THIS FIXES MAC BUTTON ISSUE)
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Custom.TButton",
    font=("Arial", 12, "bold"),
    padding=10
)


# TITLE
tk.Label(
    app,
    text="🌍 GeoLocator Pro",
    fg="white",
    bg="#111111",
    font=("Arial", 16, "bold")
).pack(pady=10)


# INPUT
entry = tk.Entry(app, width=40, font=("Arial", 12))
entry.pack(pady=10)


# BUTTON (FIXED USING TTK)
search_btn = ttk.Button(
    app,
    text="Search Location",
    command=search,
    style="Custom.TButton"
)
search_btn.pack(pady=10)


# RESULT
result_label = tk.Label(
    app,
    text="Enter a location",
    fg="white",
    bg="#111111",
    font=("Arial", 11)
)
result_label.pack(pady=10)


app.mainloop()

### Created by mehedi hasan rabby ##MHR
### GEO CODING ### PYTHON 3.24 VERSION USED