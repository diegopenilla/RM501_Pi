int impulsCount=0;
int coinHIGH = 0;
void incomingImpuls()
{
  impulsCount=impulsCount+1;
  coinHIGH = 1;
  Serial.println("Impulse detected: " + String(impulsCount));  // Send message to Raspberry Pi
}

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
  attachInterrupt(digitalPinToInterrupt(3),incomingImpuls, FALLING);
}

void loop() {

  if(coinHIGH == 1){
    digitalWrite(8, LOW);
    delay(1000*30);
    delay(1000*30);
    delay(1000*30);
    digitalWrite(8, HIGH);
    coinHIGH=0;
  }
  digitalWrite(8, HIGH);
}