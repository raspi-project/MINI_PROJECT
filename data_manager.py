from sensors import get_sensor_data
from sensors import start_mqtt
from weather import get_weather_data


def get_combined_data():
    """
    Combines sensor data and weather data
    Returns one structured dictionary for AI processing.
    """

    sensor_data = get_sensor_data()
    weather_data = get_weather_data()

    # If any error occurs in either module
    if "error" in sensor_data:
        return {"error": f"Sensor Error: {sensor_data['error']}"}

    if "error" in weather_data:
        return {"error": f"Weather Error: {weather_data['error']}"}

    # Combine both
    combined_data = {
        "soil_data": {
            "soil_moisture": sensor_data["soil"],
            "ph": sensor_data["ph"],
            "tds": sensor_data["tds"],
            "nitrogen": sensor_data["nitrogen"],
            "phosphorus": sensor_data["phosphorus"],
            "potassium": sensor_data["potassium"]
        },
        "weather_data": weather_data
    }

    return combined_data
