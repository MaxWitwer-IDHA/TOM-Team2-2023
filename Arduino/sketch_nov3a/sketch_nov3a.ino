#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

Adafruit_BNO055 bno = Adafruit_BNO055();

void setup(void)
{
  Serial.begin(115200);
  delay(1000);

  if (!bno.begin())
  {
    Serial.println("Could not find a valid BNO055 sensor, check wiring!");
    while (1);
  }

  delay(1000);

  bno.setExtCrystalUse(true);
}

void loop(void)
{
  sensors_event_t event;
  bno.getEvent(&event);

  Serial.print(event.orientation.x);
  Serial.print(",");
  Serial.print(event.orientation.y);
  Serial.print(",");
  Serial.print(event.orientation.z);
  Serial.println();

  delay(10);
}
