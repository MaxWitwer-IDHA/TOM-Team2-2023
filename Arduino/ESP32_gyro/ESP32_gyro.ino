#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

#define BNO055_I2C_ADDR 0x28 // BNO055 I2C address

Adafruit_BNO055 bno = Adafruit_BNO055(BNO055_I2C_ADDR);

void setup() {
  Serial.begin(115200);
  if (!bno.begin())
  {
    Serial.println("Could not find a valid BNO055 sensor, check wiring!");
    while (1);
  }
  bno.setExtCrystalUse(true);
}

void loop() {
  sensors_event_t orientationData;
  bno.getEvent(&orientationData);

  // Print orientation data
  Serial.print("Orientation: ");
  Serial.print(orientationData.orientation.x);
  Serial.print(" ");
  Serial.print(orientationData.orientation.y);
  Serial.print(" ");
  Serial.print(orientationData.orientation.z);
  Serial.println();

  delay(10);
}
