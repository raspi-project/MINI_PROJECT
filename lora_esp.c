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

// Define Sensor Pins (Matching the hardware table)
#define SOIL_PIN 32
#define LDR_PIN 33
#define TDS_PIN 34
#define DHTPIN 4

// Define DHT Type (DHT11)
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int counter = 0;

// =====================
// SENSOR FUNCTIONS
// =====================

// Actual Soil Moisture Sensor Reading
int readSoilMoisture() {
  int rawValue = analogRead(SOIL_PIN);
  // Map ADC value: 4095 (completely dry) to 1000 (completely wet) into 0-100%
  int moisturePercent = map(rawValue, 4095, 1000, 0, 100);
  
  // Constrain values between 0 and 100
  if(moisturePercent > 100) moisturePercent = 100;
  if(moisturePercent < 0) moisturePercent = 0;
  
  return moisturePercent; 
}

// pH Sensor
float readPH() {
  return 6.5;  // Dummy value
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

// Actual LDR (Sunlight Intensity) Reading
int readLDR() {
  int rawValue = analogRead(LDR_PIN);
  // Map ADC value: 0 (dark) to 4095 (bright) into 0-100%
  int lightPercent = map(rawValue, 0, 4095, 0, 100);
  return lightPercent;
}

// Actual TDS Sensor Reading
int readTDS() {
  int rawValue = analogRead(TDS_PIN);
  // Basic conversion: Map ADC value 0-4095 roughly to 0-1000 ppm
  int tdsValue = map(rawValue, 0, 4095, 0, 1000); 
  return tdsValue;
}

// DHT11 Temperature Reading
float readTemperature() {
  float temp = dht.readTemperature();
  // Check if any reads failed and return 0.0
  if (isnan(temp)) {
    return 0.0; 
  }
  return temp;
}

// DHT11 Humidity Reading
float readHumidity() {
  float hum = dht.readHumidity();
  // Check if any reads failed and return 0.0
  if (isnan(hum)) {
    return 0.0; 
  }
  return hum;
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender Started");

  // Initialize OLED Display (I2C address is usually 0x3C)
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever if OLED fails
  }
  
  // Show welcome screen on OLED
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.println("Farm Advisor System");
  display.println("Initializing...");
  display.display();
  delay(2000);

  // Initialize DHT sensor
  dht.begin();

  // Setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);
  
  // Set to 433 MHz to match receiver
  while (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    display.clearDisplay();
    display.setCursor(0, 10);
    display.println("LoRa Error!");
    display.display();
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
  int ldr = readLDR();
  int tds = readTDS();
  float temp = readTemperature();
  float hum = readHumidity();
  float ph = readPH();
  String npk = readNPK();

  // =====================
  // Display on Serial Monitor
  // =====================
  Serial.println("\n--- Sensor Readings ---");
  Serial.print("Soil Moisture : "); Serial.print(soil); Serial.println(" %");
  Serial.print("Sunlight (LDR): "); Serial.print(ldr); Serial.println(" %");
  Serial.print("Water TDS     : "); Serial.print(tds); Serial.println(" ppm");
  Serial.print("Temperature   : "); Serial.print(temp); Serial.println(" C");
  Serial.print("Humidity      : "); Serial.print(hum); Serial.println(" %");
  Serial.println("-----------------------");

  // =====================
  // Display on OLED
  // =====================
  display.clearDisplay();
  display.setCursor(0, 0);
  
  display.println("--- Farm Advisor ---");
  
  // Print Soil and LDR on same line to save space
  display.print("Soil:"); display.print(soil); display.print("% ");
  display.print("LDR:"); display.print(ldr); display.println("%");
  
  // Print TDS
  display.print("TDS: "); display.print(tds); display.println(" ppm");
  
  // Print Temp and Hum
  display.print("Temp: "); display.print(temp, 1); display.println(" C");
  display.print("Hum:  "); display.print(hum, 1); display.println(" %");
  
  // Print Packet Counter
  display.println("");
  display.print("Sent Pkts: "); display.print(counter);
  
  display.display();

  // =====================
  // Send via LoRa
  // =====================
  // Combine into a single, highly efficient comma-separated payload
  // Format: counter,soil(%),ldr(%),tds(ppm),temp(C),hum(%)
  String payload = String(counter) + "," + 
                   String(soil) + "," + 
                   String(ldr) + "," + 
                   String(tds) + "," + 
                   String(temp) + "," + 
                   String(hum)+ "," + 
                    npk+"," String(ph);

  Serial.print("Sending LoRa Packet: ");
  Serial.println(payload);

  // Send LoRa packet to receiver
  LoRa.beginPacket();
  LoRa.print(payload); 
  LoRa.endPacket();

  counter++;
  
  // Wait 5 seconds before sending the next packet to protect the module
  delay(5000);  
}


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
