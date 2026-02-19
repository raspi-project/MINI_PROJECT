import requests
import os
import sys
from datetime import datetime
from collections import defaultdict

# ==============================
# CONFIGURATION
# ==============================

CITY = "Jaipur"   # Change city here
API_KEY = "WEATHER_API"
# to get api -> https://openweathermap.org/api

if not API_KEY:
    print("Set API key using:")
    print('export WEATHER_API="your_api_key_here"')
    sys.exit()

# ==============================
# API URLs
# ==============================

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

params = {
    "q": CITY,
    "appid": API_KEY,
    "units": "metric"
}

try:
    # ==============================
    # CURRENT WEATHER
    # ==============================
    current_response = requests.get(CURRENT_URL, params=params, timeout=10)
    current_response.raise_for_status()
    current_data = current_response.json()

    city_name = current_data["name"]
    country = current_data["sys"]["country"]

    print("\n===================================")
    print(f"📍 Location: {city_name}, {country}")
    print("===================================")
    print("Temperature:", current_data["main"]["temp"], "°C")
    print("Feels Like:", current_data["main"]["feels_like"], "°C")
    print("Humidity:", current_data["main"]["humidity"], "%")
    print("Pressure:", current_data["main"]["pressure"], "hPa")
    print("Weather:", current_data["weather"][0]["description"].title())
    print("===================================\n")

    # ==============================
    # FORECAST DATA (Rain Probability)
    # ==============================
    forecast_response = requests.get(FORECAST_URL, params=params, timeout=10)
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    print("🌧 Rain Probability Forecast (Next 3 Days)\n")

    daily_rain = defaultdict(list)

    for entry in forecast_data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        pop = entry.get("pop", 0) * 100  # Convert to percentage
        daily_rain[date].append(pop)

    today = datetime.utcnow().date()
    days_checked = 0

    for date_str in sorted(daily_rain.keys()):
        forecast_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        if forecast_date > today and days_checked < 3:
            max_rain = max(daily_rain[date_str])
            print(f"{forecast_date} → {max_rain:.0f}% chance of rain")
            days_checked += 1

    print("\n===================================\n")

except requests.exceptions.ConnectionError:
    print("No internet connection.")
except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
except Exception as e:
    print("Error:", e)
