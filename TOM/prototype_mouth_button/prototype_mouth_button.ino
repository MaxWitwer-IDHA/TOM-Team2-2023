// void setup() {
//   Serial.begin(9600); // Initialize the serial communication
//   pinMode(buttonPin, INPUT); // Set the button pin as input
// }

// void loop() {
//   int buttonState = digitalRead(buttonPin); // Read the state of the button
  
//   if (buttonState == HIGH) { // If button is pressed
//     Serial.println("1"); // Print '1' to the serial monitor
//   } else { // If button is not pressed
//     Serial.println("0"); // Print '0' to the serial monitor
//   }

//   delay(100); // Delay to debounce the button (adjust as needed)
// }

int state = 0;
const int buttonPin = 2; // Define the pin where the button is connected

void setup() {
  pinMode(buttonPin, INPUT); // Set the button pin as input
  Serial.begin(38400); // Default communication rate of the Bluetooth module
}

void loop() {
  int buttonState = digitalRead(buttonPin); // Read the state of the button

  if (buttonState == HIGH) { // If button is pressed
    Serial.println("1"); // Print '1' to the serial monitor
  } else { // If button is not pressed
    Serial.println("0"); // Print '0' to the serial monitor
  }

}
 