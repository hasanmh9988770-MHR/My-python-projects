import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    WEATHER_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")