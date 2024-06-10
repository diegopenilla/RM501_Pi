void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

void loop() {
  // Send the string "Hello" over the serial connection:
  Serial.println("Hello");

  // Wait for a second so the message doesn't get sent too frequently:
  delay(1000);
}