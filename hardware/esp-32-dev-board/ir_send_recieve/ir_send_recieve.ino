#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <IRrecv.h>
#include <IRutils.h>

const uint16_t kIrLed = 23;
const uint16_t kRecvPin = 22;
const uint16_t kButtonPin = 0; // BOOT button

IRsend irsend(kIrLed);
IRrecv irrecv(kRecvPin);

decode_results results;

void setup() {
  Serial.begin(115200);

  pinMode(kButtonPin, INPUT_PULLUP); // important

  irsend.begin();
  irrecv.enableIRIn();
}

void loop() {
  // 🔫 Trigger pressed
  if (digitalRead(kButtonPin) == LOW) {
    Serial.println("shooting: pew pew pew");
    irsend.sendNEC(0x20DF10EF, 32);

    delay(300); // debounce / prevent spam
  }

  // 🎯 Check for hit
  if (irrecv.decode(&results)) {
    Serial.print("hit: Ouch! (raw ");
    Serial.print(resultToHexidecimal(&results));
    Serial.println(")");

    irrecv.resume();
  }
}