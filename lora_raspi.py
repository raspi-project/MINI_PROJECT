# This Code is the updated code for LDR and DHT11
# LoRa receiver code 

import sys
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])

    def start(self):
        print("LoRa Receiver Started... Waiting for sensor data.")
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(1)

    def on_rx_done(self):
        print("\nMessage Received")
        self.clear_irq_flags(RxDone=1)

        payload = self.read_payload(nocheck=True)
        message = bytes(payload).decode("utf-8", 'ignore').strip() 

        print(f"Raw String: {message}")
        print(f"RSSI: {self.get_rssi_value()} dBm")

        try:
            data_array = message.split(",")
            
            # Check for exactly 10 pieces of data
            # Format: counter, soil, ldr, tds, temp, hum, ph, N, P, K
            if len(data_array) == 10:
                packet_count  = int(data_array[0])
                soil_moisture = int(data_array[1])
                sunlight_ldr  = int(data_array[2])
                tds_value     = int(data_array[3])
                temperature   = float(data_array[4])
                humidity      = float(data_array[5])
                ph_level      = float(data_array[6])
                nitrogen      = int(data_array[7])
                phosphorus    = int(data_array[8])
                potassium     = int(data_array[9])

                print("\n📊 --- Parsed Sensor Data ---")
                print(f"Packet ID    : {packet_count}")
                print(f"Soil Moist   : {soil_moisture}%")
                print(f"Sunlight(LDR): {sunlight_ldr}%")
                print(f"Water TDS    : {tds_value} ppm")
                print(f"Temperature  : {temperature} °C")
                print(f"Humidity     : {humidity}%")
                # print(f"pH Level     : {ph_level}")
                # print(f"Nitrogen (N) : {nitrogen}")
                # print(f"Phosphor (P) : {phosphorus}")
                # print(f"Potassium(K) : {potassium}")
                print("-----------------------------\n")
                
            else:
                print(f" Warning: Received incomplete packet (Expected 10 parts, got {len(data_array)}). Ignoring.")
                
        except Exception as e:
            print(f" Error parsing data (corrupted packet): {e}")

        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


lora = LoRaRcvCont(verbose=False)

lora.set_mode(MODE.STDBY)
lora.set_freq(433.0) 
lora.set_pa_config(pa_select=1)
lora.set_sync_word(0xF3) 
lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)

try:
    lora.start()
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
    

'''
# This Code Is Working fine for without LDR and DHT11 sensor 

# LoRa receiver code 

import sys
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)

        # DIO0 -> RxDone
        self.set_dio_mapping([0,0,0,0,0,0])

    def start(self):
        print("LoRa Receiver Started... Waiting for sensor data.")

        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

        while True:
            sleep(1)

    def on_rx_done(self):
        print("\n📩 Message Received")
        self.clear_irq_flags(RxDone=1)

        # Read and decode the raw payload
        payload = self.read_payload(nocheck=True)
        message = bytes(payload).decode("utf-8", 'ignore').strip() # strip() removes hidden newlines

        print(f"Raw String: {message}")
        print(f"RSSI: {self.get_rssi_value()} dBm")

        # -----------------------------------------------------
        # DATA PARSING: Splitting the string into variables
        # -----------------------------------------------------
        try:
            # Split the string at every comma
            data_array = message.split(",")
            
            # Check if we received all 7 pieces of data
            if len(data_array) == 7:
                # Assign to individual variables and convert to correct data types
                packet_count  = int(data_array[0])
                soil_moisture = int(data_array[1])
                ph_level      = float(data_array[2])
                tds_value     = int(data_array[3])
                nitrogen      = int(data_array[4])
                phosphorus    = int(data_array[5])
                potassium     = int(data_array[6])

                # Display the variables neatly
                print("\n📊 --- Parsed Sensor Data ---")
                print(f"Packet ID   : {packet_count}")
                print(f"Soil Moist  : {soil_moisture}%")
                print(f"pH Level    : {ph_level}")
                print(f"TDS         : {tds_value} ppm")
                print(f"Nitrogen (N): {nitrogen}")
                print(f"Phosphor (P): {phosphorus}")
                print(f"Potassium(K): {potassium}")
                print("-----------------------------\n")
                
                # YOU CAN NOW USE THESE VARIABLES FOR A DATABASE, DASHBOARD, ETC.
                # example: my_database.save(ph_level)
                
            else:
                print("⚠️ Warning: Received incomplete packet. Ignoring.")
                
        except Exception as e:
            print(f"⚠️ Error parsing data (corrupted packet): {e}")

        # Restart listening for the next packet
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


lora = LoRaRcvCont(verbose=False)

# 🔥 IMPORTANT CONFIG 
lora.set_mode(MODE.STDBY)
lora.set_freq(433.0)   # Set to 433 MHz
lora.set_pa_config(pa_select=1)

# Sync Word matches the transmitter
lora.set_sync_word(0xF3) 

lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)

try:
    lora.start()

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
'''


# This code is for testing purpose only
'''
import sys
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)

        # DIO0 -> RxDone
        self.set_dio_mapping([0,0,0,0,0,0])

    def start(self):
        print("LoRa Receiver Started...")

        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

        while True:
            sleep(1)

    def on_rx_done(self):
        print("\n📩 Message Received")

        self.clear_irq_flags(RxDone=1)

        payload = self.read_payload(nocheck=True)
        message = bytes(payload).decode("utf-8", 'ignore')

        print("Data:", message)
        print("RSSI:", self.get_rssi_value())

        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)



lora = LoRaRcvCont(verbose=False)

# 🔥 IMPORTANT CONFIG (must match sender)
lora.set_mode(MODE.STDBY)
lora.set_freq(500.0)   # change if needed 500 MHz
lora.set_pa_config(pa_select=1)

lora.set_sync_word(0xF3) # <--- ADD THIS LINE HERE

lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)

try:
    lora.start()

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
'''
