// LoRa Transmitter Node (ESP32) with OLED Display

#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Define OLED parameters (128x64 display)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1 
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Define the pins used by the LoRa transceiver module
#define ss 5
#define rst 14
#define dio0 2

// Define Sensor Pins
#define SOIL_PIN 32
#define LDR_PIN 33
#define TDS_PIN 34
#define DHTPIN 4

// Define DHT Type
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int counter = 0;

// =====================
// SENSOR FUNCTIONS
// =====================

int readSoilMoisture() {
  int rawValue = analogRead(SOIL_PIN);
  int moisturePercent = map(rawValue, 4095, 1000, 0, 100);
  if(moisturePercent > 100) moisturePercent = 100;
  if(moisturePercent < 0) moisturePercent = 0;
  return moisturePercent; 
}

int readLDR() {
  int rawValue = analogRead(LDR_PIN);
  int lightPercent = map(rawValue, 0, 4095, 0, 100);
  return lightPercent;
}

int readTDS() {
  int rawValue = analogRead(TDS_PIN);
  int tdsValue = map(rawValue, 0, 4095, 0, 1000); 
  return tdsValue;
}

float readTemperature() {
  float temp = dht.readTemperature();
  if (isnan(temp)) return 0.0; 
  return temp;
}

float readHumidity() {
  float hum = dht.readHumidity();
  if (isnan(hum)) return 0.0; 
  return hum;
}

// pH Sensor (Constant)
float readPH() {
  return 6.5;  
}

// NPK Sensor (Constant)
String readNPK() {
  int nitrogen = 40;
  int phosphorus = 25;
  int potassium = 30;
  return String(nitrogen) + "," + String(phosphorus) + "," + String(potassium);
}

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender Started");

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); 
  }
  
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.println("Farm Advisor System");
  display.println("Initializing...");
  display.display();
  delay(2000);

  dht.begin();
  LoRa.setPins(ss, rst, dio0);
  
  while (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    display.clearDisplay();
    display.setCursor(0, 10);
    display.println("LoRa Error!");
    display.display();
    delay(500);
  }
  
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");
}

void loop() {
  // Read all sensors
  int soil = readSoilMoisture();
  int ldr = readLDR();
  int tds = readTDS();
  float temp = readTemperature();
  float hum = readHumidity();
  float ph = readPH();
  String npk = readNPK();

  // Print to Serial
  Serial.println("\n--- Sensor Readings ---");
  Serial.print("Soil Moisture : "); Serial.print(soil); Serial.println(" %");
  Serial.print("Sunlight (LDR): "); Serial.print(ldr); Serial.println(" %");
  Serial.print("Water TDS     : "); Serial.print(tds); Serial.println(" ppm");
  Serial.print("Temperature   : "); Serial.print(temp); Serial.println(" C");
  Serial.print("Humidity      : "); Serial.print(hum); Serial.println(" %");
  //Serial.print("pH Level      : "); Serial.println(ph);
  //Serial.print("NPK Values    : "); Serial.println(npk);
  Serial.println("-----------------------");

  // Print to OLED
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("--- Farm Advisor ---");
  
  display.print("Soil:"); display.print(soil); display.print("% ");
  display.print("LDR:"); display.print(ldr); display.println("%");
  
  display.print("TDS: "); display.print(tds); display.println(" ppm");
  
  display.print("Temp: "); display.print(temp, 1); display.println(" C");
  display.print("Hum:  "); display.print(hum, 1); display.print("% ");
  //display.print("pH:"); display.println(ph, 1);
  
  display.print("Pkts: "); display.print(counter);
  display.display();

  // Send via LoRa
  // Format: counter, soil, ldr, tds, temp, hum, ph, N, P, K
  String payload = String(counter) + "," + 
                   String(soil) + "," + 
                   String(ldr) + "," + 
                   String(tds) + "," + 
                   String(temp) + "," + 
                   String(hum) + "," + 
                   String(ph) + "," + 
                   npk;

  Serial.print("Sending LoRa Packet: ");
  Serial.println(payload);

  LoRa.beginPacket();
  LoRa.print(payload); 
  LoRa.endPacket();

  counter++;
  delay(3000);  
}

/*
this below code is for reading PH and NPK values from sensor 
#include <ModbusMaster.h>

// --- Pin Definitions ---
#define MAX485_RX      16  // Connect to RO of MAX485
#define MAX485_TX      17  // Connect to DI of MAX485
#define MAX485_RE_DE   4   // Connect to RE & DE of MAX485
#define PH_PIN         34  // Analog pin for pH sensor (GPIO 34)

// --- Constants ---
const float voltage_ref = 3.3; // ESP32 logic voltage
const int adc_resolution = 4095;

ModbusMaster node;

// Callback for RS485 flow control
void preTransmission() {
  digitalWrite(MAX485_RE_DE, HIGH);
}

void postTransmission() {
  digitalWrite(MAX485_RE_DE, LOW);
}

void setup() {
  Serial.begin(115200);
  
  // RS485 setup (Usually 9600 baud for NPK sensors)
  Serial2.begin(9600, SERIAL_8N1, MAX485_RX, MAX485_TX);
  
  pinMode(MAX485_RE_DE, OUTPUT);
  digitalWrite(MAX485_RE_DE, LOW);

  node.begin(1, Serial2); // Slave ID 1
  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  Serial.println("System Initialized. Reading Sensors...");
}

void loop() {
  readNPK();
  readPH();
  Serial.println("-----------------------");
  delay(3000);
}

void readNPK() {
  uint8_t result;
  // NPK sensors often store N, P, K in registers starting at 0x001E
  // Note: Check your specific sensor manual for the register address!
  result = node.readHoldingRegisters(0x001E, 3);

  if (result == node.ku8MBSuccess) {
    uint16_t n = node.getResponseBuffer(0);
    uint16_t p = node.getResponseBuffer(1);
    uint16_t k = node.getResponseBuffer(2);

    Serial.print("Nitrogen (N): "); Serial.print(n); Serial.println(" mg/kg");
    Serial.print("Phosphorus (P): "); Serial.print(p); Serial.println(" mg/kg");
    Serial.print("Potassium (K): "); Serial.print(k); Serial.println(" mg/kg");
  } else {
    Serial.print("Modbus Error: "); Serial.println(result, HEX);
  }
}

void readPH() {
  int adcValue = analogRead(PH_PIN);
  float voltage = (adcValue * voltage_ref) / adc_resolution;
  
  // Simple linear calibration: pH = 7 + ((V_neutral - V_actual) / slope)
  // You MUST calibrate these values for your specific sensor.
  float phValue = 3.5 * voltage; // Placeholder conversion logic

  Serial.print("Analog Voltage: "); Serial.print(voltage);
  Serial.print(" | pH Value: "); Serial.println(phValue);
}
*/




/*
// Lora Transmitter

#include <SPI.h>
#include <LoRa.h>

//define the pins used by the transceiver module
#define ss 5
#define rst 14
#define dio0 2

int counter = 0;

// =====================
// SENSOR FUNCTIONS
// =====================

// Soil Moisture Sensor
int readSoilMoisture() {
  return 65;  // Dummy value (%)
}

// pH Sensor
float readPH() {
  return 6.5;  // Dummy value
}

// TDS Sensor
int readTDS() {
  return 450;  // Dummy value (ppm)
}

// NPK Sensor
String readNPK() {
  int nitrogen = 40;
  int phosphorus = 25;
  int potassium = 30;

  return String(nitrogen) + "," + 
         String(phosphorus) + "," + 
         String(potassium);
}

void setup() {
  //initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender Started");

  //setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);
  
  // Set to 433 MHz to match receiver
  while (!LoRa.begin(433E6)) {
    Serial.println(".");
    delay(500);
  }
  
  // Change sync word to match the receiver
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");
}

void loop() {
  // =====================
  // Read Sensor Values
  // =====================
  int soil = readSoilMoisture();
  float ph = readPH();
  String npk = readNPK();
  int tds = readTDS();

  // Combine into a single, highly efficient comma-separated payload
  // Format: counter,soil,ph,tds,N,P,K
  String payload = String(counter) + "," + String(soil) + "," + "," + String(tds) + "," + npk+ String(ph) ;

  Serial.print("Sending packet: ");
  Serial.println(payload);

  // Send LoRa packet to receiver
  LoRa.beginPacket();
  LoRa.print(payload); 
  LoRa.endPacket();

  counter++;
  
  // Wait 5 seconds before sending the next packet to protect the module
  delay(5000);  
}
*/


// This code is for testing purpose 
/*
#include <SPI.h>
#include <LoRa.h>

//define the pins used by the transceiver module
#define ss 5
#define rst 14
#define dio0 2

int counter = 0;

void setup() {
  //initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender");

  //setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);
  
  //replace the LoRa.begin(---E-) argument with your location's frequency 
  //433E6 for Asia
  //868E6 for Europe
  //915E6 for North America
  while (!LoRa.begin(500E6)) {
    Serial.println(".");
    delay(500);
  }
   // Change sync word (0xF3) to match the receiver
  // The sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");
}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);

  //Send LoRa packet to receiver
  LoRa.beginPacket();
  LoRa.print("hello From Sirvi ESP");
  LoRa.println("");
  LoRa.print(counter);
  LoRa.endPacket();

  counter++;

  delay(500);
}
*/
