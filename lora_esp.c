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
  int tds = readTDS();
  String npk = readNPK();

  // Combine into a single, highly efficient comma-separated payload
  // Format: counter,soil,ph,tds,N,P,K
  String payload = String(counter) + "," + String(soil) + "," + String(ph) + "," + String(tds) + "," + npk;

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
