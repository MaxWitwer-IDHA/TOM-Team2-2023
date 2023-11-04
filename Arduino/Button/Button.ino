const int buttonPin = 27; // Define the digital pin for the button
int buttonState = 0;      // Variable to store the button state (0 for LOW, 1 for HIGH)

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
  // Set the button pin as an input
  pinMode(buttonPin, INPUT);
}

void loop() {
  // Read the state of the button
  buttonState = digitalRead(buttonPin);

  // Print the button state to the serial monitor
  Serial.print("Button state: ");
  Serial.println(buttonState);

  // You can add a short delay to prevent rapid serial output
  delay(100);
}
