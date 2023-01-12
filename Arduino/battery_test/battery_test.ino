#include "battery.h"

void setup() {
    Serial.begin(9600);
}

void loop() {

    Serial.println(read_battery());	
    delay(200);
}
