// 1. Ready Mode - Green Light -> Coin Ready to be given
// 2. Operating Mode - Yellow Light -> After coin is given
// 3. Error Mode - counter reaches maximum sticker number
// 4. App Mode - blue light

// Button 1 sets counter to 0 or 20
// if counter is 20 - error mode is active, at which no action can be done

// Machine has 20 a capacity of 20 stickers
// > Counter (starts at 0) and increases +1 every time a coin is given (ready + operating mode)
// > When the counter reaches 20, error mode is active ( error mode): the user needs to replace manually the stickers and press Button UP.

// Button Up - Sets counter to 0 or 20 -> triggering the machine to be ready or in error mode.

// Button Down - Sets app mode

#include <Adafruit_NeoPixel.h>

int maxStickers = 20;
int stickerCoreoDuration = 3000;

// Button and LED configuration
const int coinPin = 2; // pin to read signal from coin acceptor
const int button1Pin = 8;  // the number of the first pushbutton pin
const int button2Pin = 9;  // the number of the second pushbutton pin
int button1State = 0;      // variable for reading the first pushbutton status
int button2State = 0;      // variable for reading the second pushbutton status
int lastButton1State = HIGH; // previous state of the first pushbutton
int lastButton2State = HIGH; // previous state of the second pushbutton
bool button1On = false;    // current state of button 1 (ON/OFF)
bool button2On = false;    // current state of button 2 (ON/OFF)
int counter = 0;           // counter variable

int relayPin = 11;
bool relayState = LOW;

#define LED_PIN1 3
#define LED_PIN2 4
#define LED_PIN3 5
#define LED_PIN4 6
#define NUM_LEDS 120
#define NUM_LEDS2 60
#define NUM_LEDS_IN
#define BRIGHTNESS 10

// Define NeoPixel strips
Adafruit_NeoPixel strip1 = Adafruit_NeoPixel(NUM_LEDS, LED_PIN1, NEO_RGBW + NEO_KHZ800);
Adafruit_NeoPixel strip2 = Adafruit_NeoPixel(NUM_LEDS, LED_PIN2, NEO_RGBW + NEO_KHZ800);
Adafruit_NeoPixel strip3 = Adafruit_NeoPixel(NUM_LEDS, LED_PIN3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip4 = Adafruit_NeoPixel(NUM_LEDS, LED_PIN4, NEO_RGB + NEO_KHZ800);

int impulsCount = 0;
volatile int coinHIGH = 0;
int appMode = 0;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50; // milliseconds

void incomingImpuls() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTime) > debounceDelay) {
    impulsCount++;
    coinHIGH = 1;
    Serial.println("Impulse detected: " + String(impulsCount));  // Send message to Raspberry Pi
    counter++;
    lastDebounceTime = currentTime;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(coinPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(coinPin), incomingImpuls, FALLING);

  // Initialize the NeoPixel strips
  strip1.begin();
  strip1.setBrightness(BRIGHTNESS);
  strip1.show(); // Initialize all pixels to 'off'

  strip2.begin();
  strip2.setBrightness(BRIGHTNESS);
  strip2.show(); // Initialize all pixels to 'off'

  strip3.begin();
  strip3.setBrightness(BRIGHTNESS);
  strip3.show(); // Initialize all pixels to 'off'

  strip4.begin();
  strip4.setBrightness(BRIGHTNESS);
  strip4.show(); // Initialize all pixels to 'off'

  // initialize the pushbutton pins as inputs with the internal pull-up resistors enabled
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Ensure relay starts off
}

void loop() {
  // read the state of the pushbutton values
  button1State = digitalRead(button1Pin);
  button2State = digitalRead(button2Pin);

  // check if the first pushbutton state has changed
  if (button1State != lastButton1State) {
    // if the button state is LOW, it means the button is pressed
    if (button1State == LOW) {
      // toggle the state of button1On
      button1On = !button1On;
      // print the state of button1On
      Serial.println("Button 1 Pressed");
      // if button1On is true, set the counter to 20; if false, reset the counter to 0
      if (button1On) {
        counter = 20;
      } else {
        counter = 0;
      }
    }
    // update the last button state
    lastButton1State = button1State;
    appMode = 0;
  }

  // check if the second pushbutton state has changed
  if (button2State != lastButton2State) {
    // if the button state is LOW, it means the button is pressed
    if (button2State == LOW) {
      // toggle the state of button2On
      button2On = !button2On;
      // send the message "app" via serial print
      appMode = !appMode;
      Serial.println("app" + String(appMode));
    }
    // update the last button state
    lastButton2State = button2State;
  }

  if (counter >= maxStickers) {
    Serial.println("Error Mode");
    setAllRed();
    if (relayState == LOW) {
      digitalWrite(relayPin, LOW);
      relayState = LOW;
    }
    coinHIGH = 0;
  } else {
    if (coinHIGH == 1) {
      Serial.println("Operating Mode");
      setAllYellow();
      Serial.println("coin");
      delay(stickerCoreoDuration); // TODO: MEASURE CHOREOGRAPHY TIME
      coinHIGH = 0;
    }
    if (appMode == 1) {
      Serial.println("App Mode Active");
      setAllBlue();
      delay(100);
    } else {
      Serial.println("Ready Mode");
      setAllGreen(); // Ensure the LEDs start as green
      // if (relayState == LOW) {
      //   digitalWrite(relayPin, HIGH);
      //   relayState = HIGH;
      // }
    }
  }

  delay(100);
}

// Function to set all LEDs to green
void setAllGreen() {
  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    strip1.setPixelColor(i, strip1.Color(255, 0, 30, 0)); // Green
    strip3.setPixelColor(i, strip3.Color(255, 0, 30, 0)); // Green
    strip4.setPixelColor(i, strip4.Color(255, 0, 30, 0)); // Green

    if (i > NUM_LEDS2 / 2) {
      strip2.setPixelColor(i, strip2.Color(255, 0, 30, 0)); // Green for first half
    } else {
      strip2.setPixelColor(i, strip2.Color(0, 0, 0, 0)); // Off for second half
    }
  }
  strip1.show();
  strip2.show();
  strip3.show();
  strip4.show();
}


// Function to set all LEDs to yellow
void setAllYellow() {
  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    strip1.setPixelColor(i, strip1.Color(120, 255, 0, 0)); // Yellow
    strip2.setPixelColor(i, strip2.Color(0, 0, 0, 0)); // Yellow
    strip3.setPixelColor(i, strip3.Color(120, 255, 0, 0)); // Yellow
    strip4.setPixelColor(i, strip4.Color(120, 255, 0, 0)); // Yellow
  }
  strip1.show();
  strip2.show();
  strip3.show();
  strip4.show();
}

// Function to set all LEDs to red
void setAllRed() {
  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    strip1.setPixelColor(i, strip1.Color(0, 255, 0, 0)); // Red
    strip3.setPixelColor(i, strip3.Color(0, 255, 0, 0)); // Red
    strip4.setPixelColor(i, strip4.Color(0, 255, 0, 0)); // Red

    if (i > NUM_LEDS2 / 2) {
      strip2.setPixelColor(i, strip2.Color(0, 0, 0, 0)); // Off for first half
    } else {
      strip2.setPixelColor(i, strip2.Color(0, 255, 0, 0)); // Red for second half
    }
  }
  strip1.show();
  strip2.show();
  strip3.show();
  strip4.show();
}


void setAllBlue() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip1.setPixelColor(i, strip1.Color(0, 0, 255));
    strip2.setPixelColor(i, strip2.Color(0, 0, 0));
    strip3.setPixelColor(i, strip3.Color(0, 0, 255));
    strip4.setPixelColor(i, strip4.Color(0, 0, 255));
  }
  strip1.show();
  strip2.show();
  strip3.show();
  strip4.show();
}
