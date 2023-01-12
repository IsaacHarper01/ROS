#include "encoders.h"

void setup(){
    set_encoders_input();
    Serial.begin(9600);
}

void loop(){
    Serial.print("Left: ");
    Serial.print(left_count());
    Serial.print("\tRight: ");
    Serial.println(right_count());
    delay(20);
}
