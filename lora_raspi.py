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
