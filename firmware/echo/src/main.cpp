#include <Arduino.h>

void setup() {
  Serial.begin(115200); // virtual on rp2040
}

void loop() {
  if(Serial.available() > 0){
    Serial.write(Serial.read());
  }
}
