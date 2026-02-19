import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
TOPIC = "farm/sensors"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print("\n===== Sensor Data Received =====")

    data = json.loads(msg.payload.decode())

    print("Soil Moisture :", data["soil"], "%")
    print("pH Level      :", data["ph"])
    print("TDS           :", data["tds"], "ppm")

    npk_values = data["npk"].split(",")
    print("Nitrogen (N)  :", npk_values[0])
    print("Phosphorus (P):", npk_values[1])
    print("Potassium (K) :", npk_values[2])

    print("=================================")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
