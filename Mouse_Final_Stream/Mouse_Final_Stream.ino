#include <BluetoothSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

Adafruit_BNO055 bno = Adafruit_BNO055();

BluetoothSerial SerialBT;

const int buttonPin = 27; // Button pin

String x = "0.0";
String y = "0.0";
String z = "0.0";
String buttonState = "0";

String bluetooth_stream;

void setup() {
  SerialBT.begin("Remy");
  Serial.begin(115200);

  pinMode(buttonPin, INPUT);

  if (!bno.begin())
  {
    Serial.println("Could not find a valid BNO055 sensor, check wiring!");
    while (1);
  }

  delay(1000);

  bno.setExtCrystalUse(true);
}

void loop() {
  // tryReconnect();

  buttonState = digitalRead(buttonPin);

  sensors_event_t event;
  bno.getEvent(&event);

  x = event.orientation.x;
  y = event.orientation.y;
  z = event.orientation.z;

  bluetooth_stream = x + "," + y + "," + z + "," + buttonState;
  SerialBT.println(bluetooth_stream);
  delay(10);


}

// void tryReconnect() {
//   if (!SerialBT.connected()) {
//     SerialBT.begin("Remy"); // Re-initialize Bluetooth
//   }
// }

