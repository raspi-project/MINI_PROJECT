from sensors import get_sensor_data
from sensors import start_lora
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

    # Combine both local hardware sensor data and internet weather data
    combined_data = {
        "local_sensor_data": {
            "soil_moisture": sensor_data["soil"],
            "sunlight_ldr": sensor_data["ldr"],
            "water_tds": sensor_data["tds"],
            "local_temperature": sensor_data["temperature"],
            "local_humidity": sensor_data["humidity"],
            "ph": sensor_data["ph"],
            "nitrogen": sensor_data["nitrogen"],
            "phosphorus": sensor_data["phosphorus"],
            "potassium": sensor_data["potassium"]
        },
        "weather_data": weather_data
    }

    return combined_data
    
'''
# This code is working fine without LDR and DHT11
from sensors import get_sensor_data
from sensors import start_lora
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
'''
