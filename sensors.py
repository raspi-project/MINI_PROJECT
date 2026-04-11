# This code with LDR and DHT11
import sys
import threading
import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

# Setup the GPIO pins for the LoRa module
BOARD.setup()

latest_sensor_data = None
lora_started = False  # Prevent multiple threads from starting

# ==============================
# LORA LISTENER CLASS
# ==============================
class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            time.sleep(0.5)

    def on_rx_done(self):
        global latest_sensor_data
        self.clear_irq_flags(RxDone=1)
        
        try:
            # Read and decode the payload
            payload = self.read_payload(nocheck=True)
            message = bytes(payload).decode("utf-8", 'ignore').strip()
            
            # Split the comma-separated string from the ESP32
            # Expected Format: counter, soil, ldr, tds, temp, hum, ph, N, P, K
            data_array = message.split(",")
            
            if len(data_array) == 10:
                # Update the global dictionary with all 10 values
                latest_sensor_data = {
                    "packet_id": int(data_array[0]),
                    "soil": int(data_array[1]),
                    "ldr": int(data_array[2]),
                    "tds": int(data_array[3]),
                    "temperature": float(data_array[4]),
                    "humidity": float(data_array[5]),
                    "ph": float(data_array[6]),
                    "nitrogen": int(data_array[7]),
                    "phosphorus": int(data_array[8]),
                    "potassium": int(data_array[9])
                }
                # Optional: Print to verify it's updating in the background
                # print(f"✅ LoRa Updated: {latest_sensor_data}")
                
        except Exception as e:
            # Silently ignore corrupted packets to prevent crashing
            pass 

        # Resume listening
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

# ==============================
# START LORA (Background Thread)
# ==============================
def _run_lora_loop():
    """ This function runs entirely in a background thread """
    lora = LoRaRcvCont(verbose=False)
    
    # Configure parameters to match ESP32
    lora.set_mode(MODE.STDBY)
    lora.set_freq(433.0)
    lora.set_pa_config(pa_select=1)
    lora.set_sync_word(0xF3)
    lora.set_spreading_factor(7)
    lora.set_bw(BW.BW125)
    lora.set_coding_rate(CODING_RATE.CR4_5)
    
    try:
        print("LoRa Background Listener Started...")
        lora.start()
    except KeyboardInterrupt:
        pass
    finally:
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()

def start_lora():
    """ Starts the background thread (similar to mqtt.loop_start) """
    global lora_started

    if lora_started:
        return  # Prevent restarting

    # Create a daemon thread so it closes cleanly when the main script ends
    lora_thread = threading.Thread(target=_run_lora_loop, daemon=True)
    lora_thread.start()
    
    lora_started = True

# ==============================
# GET SENSOR DATA
# ==============================
def get_sensor_data():
    """
    Returns latest sensor data.
    Starts LoRa automatically if not started.
    """
    start_lora()

    # Wait until first data is received
    timeout = 15  # seconds (slightly longer wait for LoRa since ESP sends every 5s)
    waited = 0

    while latest_sensor_data is None and waited < timeout:
        time.sleep(1)
        waited += 1

    if latest_sensor_data is None:
        return {"error": "No sensor data received via LoRa"}

    return latest_sensor_data
    
# ==============================
# TESTING MODE
# ==============================
if __name__ == "__main__":
    # If you run this file directly, it will test the background updating
    print("Testing LoRa Data Fetching...")
    
    # Start the background listener
    start_lora()
    
    # Continuously grab the latest data every few seconds
    while True:
        try:
            data = get_sensor_data()
            print("\n--- Main Thread Processing ---")
            print("Current Data:", data)
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
            


'''
# This code was working Fine without ldr and dht11
import sys
import threading
import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

# Setup the GPIO pins for the LoRa module
BOARD.setup()

latest_sensor_data = None
lora_started = False  # Prevent multiple threads from starting

# ==============================
# LORA LISTENER CLASS
# ==============================
class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            time.sleep(0.5)

    def on_rx_done(self):
        global latest_sensor_data
        self.clear_irq_flags(RxDone=1)
        
        try:
            # Read and decode the payload
            payload = self.read_payload(nocheck=True)
            message = bytes(payload).decode("utf-8", 'ignore').strip()
            
            # Split the comma-separated string from the ESP32
            # Expected Format: counter,soil,ph,tds,N,P,K
            data_array = message.split(",")
            
            if len(data_array) == 7:
                # Update the global dictionary exactly like the MQTT code did
                latest_sensor_data = {
                    "packet_id": int(data_array[0]),
                    "soil": int(data_array[1]),
                    "ph": float(data_array[2]),
                    "tds": int(data_array[3]),
                    "nitrogen": int(data_array[4]),
                    "phosphorus": int(data_array[5]),
                    "potassium": int(data_array[6])
                }
                # Optional: Print to verify it's updating in the background
                # print(f"✅ LoRa Updated: {latest_sensor_data}")
                
        except Exception as e:
            # Silently ignore corrupted packets to prevent crashing
            pass 

        # Resume listening
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

# ==============================
# START LORA (Background Thread)
# ==============================
def _run_lora_loop():
    """ This function runs entirely in a background thread """
    lora = LoRaRcvCont(verbose=False)
    
    # Configure parameters to match ESP32
    lora.set_mode(MODE.STDBY)
    lora.set_freq(433.0)
    lora.set_pa_config(pa_select=1)
    lora.set_sync_word(0xF3)
    lora.set_spreading_factor(7)
    lora.set_bw(BW.BW125)
    lora.set_coding_rate(CODING_RATE.CR4_5)
    
    try:
        print("LoRa Background Listener Started...")
        lora.start()
    except KeyboardInterrupt:
        pass
    finally:
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()

def start_lora():
    """ Starts the background thread (similar to mqtt.loop_start) """
    global lora_started

    if lora_started:
        return  # Prevent restarting

    # Create a daemon thread so it closes cleanly when the main script ends
    lora_thread = threading.Thread(target=_run_lora_loop, daemon=True)
    lora_thread.start()
    
    lora_started = True

# ==============================
# GET SENSOR DATA
# ==============================
def get_sensor_data():
    """
    Returns latest sensor data.
    Starts LoRa automatically if not started.
    """
    start_lora()

    # Wait until first data is received
    timeout = 15  # seconds (slightly longer wait for LoRa since ESP sends every 5s)
    waited = 0

    while latest_sensor_data is None and waited < timeout:
        time.sleep(1)
        waited += 1

    if latest_sensor_data is None:
        return {"error": "No sensor data received via LoRa"}

    return latest_sensor_data
    
# ==============================
# TESTING MODE
# ==============================
if __name__ == "__main__":
    # If you run this file directly, it will test the background updating
    print("Testing LoRa Data Fetching...")
    
    # Start the background listener
    start_lora()
    
    # Continuously grab the latest data every few seconds
    while True:
        try:
            data = get_sensor_data()
            print("\n--- Main Thread Processing ---")
            print("Current Data:", data)
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
'''




'''import paho.mqtt.client as mqtt
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
'''





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
