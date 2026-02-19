import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "farm/sensors"

latest_sensor_data = None
mqtt_started = False  # Prevent multiple starts

# ==============================
# MQTT CALLBACKS
# ==============================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code:", rc)
        
def on_message(client, userdata, msg):
    global latest_sensor_data

    try:
        data = json.loads(msg.payload.decode())
        npk_values = data["npk"].split(",")

        latest_sensor_data = {
            "soil": int(data["soil"]),
            "ph": float(data["ph"]),
            "tds": int(data["tds"]),
            "nitrogen": int(npk_values[0]),
            "phosphorus": int(npk_values[1]),
            "potassium": int(npk_values[2])
        }

    except Exception as e:
        print("Error processing MQTT message:", e)


# ==============================
# START MQTT (Background)
# ==============================

def start_mqtt():
    global mqtt_started

    if mqtt_started:
        return  # Prevent restarting

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    mqtt_started = True


# ==============================
# GET SENSOR DATA
# ==============================
def get_sensor_data():
    """
    Returns latest sensor data.
    Starts MQTT automatically if not started.
    """

    start_mqtt()

    # Wait until first data is received
    timeout = 10  # seconds
    waited = 0

    while latest_sensor_data is None and waited < timeout:
        time.sleep(1)
        waited += 1

    if latest_sensor_data is None:
        return {"error": "No sensor data received"}

    return latest_sensor_data
    
# ==============================
# TESTING MODE
# ==============================

if __name__ == "__main__":
    start_mqtt()
    data = get_sensor_data()
    print(data)






# ------ Below code is working fine for receveing data from raspi using mqtt-------

# import paho.mqtt.client as mqtt
# import json

# BROKER = "localhost"
# TOPIC = "farm/sensors"

# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT Broker")
#     client.subscribe(TOPIC)

# def on_message(client, userdata, msg):
#     print("\n===== Sensor Data Received =====")

#     data = json.loads(msg.payload.decode())

#     print("Soil Moisture :", data["soil"], "%")
#     print("pH Level      :", data["ph"])
#     print("TDS           :", data["tds"], "ppm")

#     npk_values = data["npk"].split(",")
#     print("Nitrogen (N)  :", npk_values[0])
#     print("Phosphorus (P):", npk_values[1])
#     print("Potassium (K) :", npk_values[2])

#     print("=================================")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(BROKER, 1883, 60)
# client.loop_forever()
