// COUNTER not COIN ... -.-

int impulsCount=0;
int coinHIGH = 0;

void incomingImpuls()
{
  Serial.println("Calling: ");
  impulsCount=impulsCount+1;
  coinHIGH = 1;
}

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
  attachInterrupt(digitalPinToInterrupt(3),incomingImpuls, FALLING);
}

void loop() {

  if(coinHIGH == 1){
    Serial.println("SLEEPING 45s on HIGH");
    digitalWrite(8, LOW);
    delay(1000*30);
    delay(1000*30);
    delay(1000*30);
    digitalWrite(8, HIGH);
    coinHIGH=0;
  }
  Serial.println(impulsCount);
  digitalWrite(8, HIGH);
}
