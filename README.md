# 🌾 Real-Time Farm Advisor System (IoT + AI)

Welcome to the **Real-Time Farm Advisor System**! This is a comprehensive Smart Agriculture solution that combines Internet of Things (IoT) edge sensors, Long-Range (LoRa) wireless communication, and Artificial Intelligence (OpenAI) to take the guesswork out of farming. 

Instead of relying on blind automated schedules, this system fuses **local field telemetry** (soil moisture, sunlight, water quality) with **internet weather forecasts** to generate conversational, highly contextual farming advice.

## ✨ Key Features
* **Long-Range Off-Grid Telemetry:** Uses SX1278 LoRa modules (433MHz) to transmit sensor data over several kilometers, eliminating the need for Wi-Fi in large crop fields.
* **Predictive AI Decision Engine:** Integrates OpenAI's LLM to analyze hardware sensor data against upcoming rain forecasts, preventing water wastage.
* **On-Site OLED Diagnostics:** Live sensor readings and packet transmission status are displayed on a local SSD1306 OLED screen in the field.
* **Real-Time Web Dashboard:** A responsive Flask-based web interface hosted on a Raspberry Pi for farmers to monitor crops and chat with the AI assistant.

---

## 🛠️ Hardware Architecture
The system is divided into two distinct nodes:

### 1. Field Node (Transmitter)
* **Microcontroller:** ESP32-DevKitC V4
* **Wireless:** SX1278 LoRa Ra-02 Module
* **Display:** 0.96" SSD1306 OLED Display (I2C)
* **Sensors:** * Soil Moisture Sensor (Analog)
  * LDR Sunlight Sensor (Analog - voltage divider)
  * Gravity TDS Meter V1.0 (Analog)
  * DHT11 Temperature & Humidity Sensor (Digital)

### 2. Server Node (Receiver & Gateway)
* **Microcomputer:** Raspberry Pi 3 Model B+ (or newer)
* **Wireless:** SX1278 LoRa Ra-02 Module

---

## 💻 Software Stack
* **C / Arduino IDE:** Firmware for the ESP32 to handle analog-to-digital conversions, sensor smoothing, and LoRa packet structuring.
* **Python 3:** Backend logic on the Raspberry Pi handling SPI LoRa reception and data parsing.
* **Flask Server:** Local Python web framework to serve the frontend dashboard.
* **OpenAI API:** For Natural Language Processing and dynamic agronomy advice.
* **Weather API:** (e.g., OpenWeatherMap) to fetch 3-day rainfall predictions.
* **HTML/CSS/JS:** Frontend UI for the farmer dashboard.

---

## 🔌 Circuit Pinouts

### ESP32 Field Node Connections
| Component | Pin Name | ESP32 GPIO |
| :--- | :--- | :--- |
| **LoRa SX1278** | 
| | NSS / CS | GPIO 5 |
| | RST | GPIO 14 |
| | DIO0 | GPIO 2 |
| | MOSI | GPIO 23 |
| | MISO | GPIO 19 |
| | SCK | GPIO 18 |
| **OLED (I2C)** | SDA | GPIO 21 |
| | SCL | GPIO 22 |
| **Sensors** | 
| |Soil Moisture (A0) | GPIO 32 |
| | LDR Sunlight (A0) | GPIO 33 |
| | TDS Meter (A0) | GPIO 34 |
| | DHT11 (Data) | GPIO 4 |

*(Note: All LoRa and OLED VCC pins are connected to 3.3V, NOT 5V).*

---

## 🚀 Installation & Setup Instructions

### Step 1: ESP32 Setup
1. Open the `ESP32_Transmitter.ino` file in the Arduino IDE.
2. Install the required libraries via the Library Manager:
   * `LoRa` by Sandeep Mistry
   * `DHT sensor library` by Adafruit
   * `Adafruit SSD1306` and `Adafruit GFX Library`
3. Connect the ESP32, select the correct COM port, and upload the code.

### Step 2: Raspberry Pi Setup
1. Enable SPI on your Raspberry Pi: `sudo raspi-config` -> Interfacing Options -> SPI -> Enable.
2. Clone this repository to your Pi:
   ```bash
   git clone [https://github.com/YourUsername/Real-Time-Farm-Advisor.git](https://github.com/YourUsername/Real-Time-Farm-Advisor.git)
   cd Real-Time-Farm-Advisor
3. Install the required Python dependencies:
   ```bash
   pip install flask openai spidev RPi.GPIO

4. Note: You will also need the pyLoRa (SX127x) library configured for Python 3.

Step 3: API Configuration
1. Open the backend Python scripts (app.py or weather.py).

2. Replace the placeholder API keys with your actual keys:
   * OPENAI_API_KEY = "your_openai_key_here"
   * WEATHER_API_KEY = "your_weather_api_key_here"

Step 4: Run the System
1. Power up the ESP32 via a battery or power bank. You should see the OLED display initialize and start showing sensor values.

2. Run the main Flask application on the Raspberry Pi:
   ```bash
   python3 app.py
3. Open a web browser on any device connected to the same Wi-Fi network and navigate to:
   ```bash
   http://<Raspberry_Pi_IP_Address>:5000

## 🔮 Future Scope
* Automated Actuation: Adding relays to the ESP32 node to allow the AI to automatically switch water pumps ON/OFF.

* Voice-Enabled Audio Advisory System: To further enhance accessibility and user experience, an integrated audio output module

* Computer Vision: Integrating a Pi Camera for early crop disease detection using CNNs.

* Solar Power Integration: Adding an MPPT solar charge controller to make the field node 100% self-sustaining.

Regional Languages: Upgrading the AI prompt to converse in local regional languages for accessibility.
