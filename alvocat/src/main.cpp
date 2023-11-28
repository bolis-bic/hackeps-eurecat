#include <Arduino.h>
#include <DHTesp.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define SERIAL_RATE 115200
#define DHT11_PIN D0
#define ANALOG_PIN A0
#define DISTANCE_TRIGGER D1
#define DISTANCE_ECHO D2
#define WATER_PUMP D3

DHTesp DHT_SENSOR;

const char* MQTT_SERVER = "84.88.76.18";
const int   MQTT_PORT = 1883;
const char* MQTT_USER = "regimiento_horticola";
const char* MQTT_PWD = "R3g1m3nt0H0rt@";

const char* DEVICE_ID = "planta1";

const char* TEMPERATURE_TOPIC = "temperature";
const char* HUMIDITY_TOPIC = "air_humidity";
const char* MOISTURE_TOPIC = "ground_humidity";
const char* DISTANCE_TOPIC = "height_distance";

char msg_topic[40];
char msg_value[4];
long value;
void callback(char* topic, byte* payload, unsigned int length);

WiFiClient espClient;
PubSubClient client(MQTT_SERVER, MQTT_PORT, callback, espClient);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");
unsigned long epochTime;

unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

void dht_initialize() {
    DHT_SENSOR.setup(DHT11_PIN, DHT_SENSOR.DHT11);
}

float dht_humidity() {
    return DHT_SENSOR.getHumidity();
}

float dht_temperature() {
    return DHT_SENSOR.getTemperature();
}

void moisture_initialize() {
    pinMode(ANALOG_PIN, INPUT);
}

float moisture() {
    return analogRead(ANALOG_PIN);
}

void distance_initialize() {
    pinMode(DISTANCE_TRIGGER, OUTPUT);
    pinMode(DISTANCE_ECHO, INPUT);
}

void distance_trig() {
    digitalWrite(DISTANCE_TRIGGER, LOW);
    delayMicroseconds(2);
    digitalWrite(DISTANCE_TRIGGER, HIGH);
    delayMicroseconds(5);
    digitalWrite(DISTANCE_TRIGGER, LOW);
}

float distance_echo() {
    long duration = pulseIn(DISTANCE_ECHO, HIGH);
    return (float)(duration * 0.034 / 2); // cm
}

void pump_initialize() {
    pinMode(WATER_PUMP, OUTPUT);
}

void pump_start() {
    digitalWrite(WATER_PUMP, HIGH);
}

void pump_end() {
    digitalWrite(WATER_PUMP, LOW);
}

int distance() {
    distance_trig();
    return distance_echo();
}

void WIFI_initialize() {
    WiFi.begin("unsecure_proxy", "ruc123jajaja");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();

    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
}

void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("client-rh", MQTT_USER, MQTT_PWD)) {

            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }

    char subscribe_topic[40];

    sprintf(subscribe_topic, "hackeps/RH/actions/%s/water_pump", DEVICE_ID);

    client.setCallback(callback);
    client.subscribe(subscribe_topic, 1);
}

void callback(char* topic, byte* payload, unsigned int length) {
    if (payload[0] == '0') {
        pump_end();
        Serial.println("--0");
    } else if (payload[0] == '1') {
        pump_start();
        Serial.println("--1");
    }
}

void MQTT_intialize() {
    reconnect();
}

void setup() {
    Serial.begin(SERIAL_RATE);
    dht_initialize();
    moisture_initialize();
    distance_initialize();
    pump_initialize();
    WIFI_initialize();
    MQTT_intialize();
}

void publish_procedure(const char* device_id, const char* topic, float value) {
    sprintf (msg_topic, "hackeps/RH/measurements/%s/%s", device_id, topic);
    StaticJsonDocument<300> jsonDoc;
    jsonDoc["value"] = (int)value;
    jsonDoc["unix_timestamp"] = getTime();
    String payload = "";
    serializeJson(jsonDoc, payload);
    client.publish(msg_topic, (char*)payload.c_str());

}


void loop() {
    client.loop();


    if (!client.connected()) {
        reconnect();
    }

    float t = dht_temperature();
    publish_procedure(DEVICE_ID, TEMPERATURE_TOPIC, t);
    delay(500);
    
    float h = dht_humidity();
    publish_procedure(DEVICE_ID, HUMIDITY_TOPIC, h);
    delay(500);
    
    float m = moisture();
    publish_procedure(DEVICE_ID, MOISTURE_TOPIC, m);
    delay(500);
    
    int d = distance();
    publish_procedure(DEVICE_ID, DISTANCE_TOPIC, d);
    delay(500);


}