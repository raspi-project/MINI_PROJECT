#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// =====================
// WiFi Credentials
// =====================
const char* ssid = "WIFI SSID";
const char* password = "PaasWord";

// =====================
// MQTT Broker (Raspberry Pi IP)
// =====================
const char* mqtt_server = "PI_IP";  // Replace with Pi IP

WiFiClient espClient;
PubSubClient client(espClient);

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

// =====================
// MQTT CONNECTION
// =====================
void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT... ");

    if (client.connect("ESP8266_Node")) {
      Serial.println("Connected!");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 2 sec");
      delay(2000);
    }
  }
}


void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("Starting ESP8266...");
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqtt_server, 1883);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  // =====================
  // Read Sensor Values
  // =====================

  int soil = readSoilMoisture();
  float ph = readPH();
  int tds = readTDS();
  String npk = readNPK();

  // Create JSON payload
  String payload = "{";
  payload += "\"soil\":" + String(soil) + ",";
  payload += "\"ph\":" + String(ph) + ",";
  payload += "\"tds\":" + String(tds) + ",";
  payload += "\"npk\":\"" + npk + "\"";
  payload += "}";

  // Publish to topic
  client.publish("farm/sensors", payload.c_str());

  Serial.println("Data Sent:");
  Serial.println(payload);
  Serial.println("----------------------");

  delay(5000);  // Send every 5 seconds
}
