def generate_alerts(weather_data):
    alerts = []

    main = weather_data.get("main", {})
    wind = weather_data.get("wind", {})

    temp = main.get("temp")
    wind_speed = wind.get("speed")

    if temp and temp > 35:
        alerts.append("🔥 Extreme Heat Warning")

    if wind_speed and wind_speed > 10:
        alerts.append("💨 Strong Wind Warning")

    return alerts