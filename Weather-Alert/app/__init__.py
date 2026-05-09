import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load API key from .env
    app.config["WEATHER_API_KEY"] = os.getenv("OPEN_WEATHER_MAP_API_KEY")

    from app.routes import main
    app.register_blueprint(main)

    return app