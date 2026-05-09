from flask import Blueprint, render_template, request
from app.weather import get_weather
from app.utils import format_city

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    weather = None
    alerts = []

    if request.method == "POST":
        city = format_city(request.form.get("city"))

        if city:
            data = get_weather(city)

            # SAFE CHECK
            if data and data.get("cod") == 200:
                weather = data
            else:
                weather = None

    return render_template("index.html", weather=weather, alerts=alerts)