#include "motors_speed.h"

int time = 200;

void setup() {
  set_motors();

  delay(1500);
  int i=0;
  Serial.begin(9600);

  while(i<time)
  {
    motors_speed(-0.07, 0.07);
  
   
    i++;
    delay(20);
  }

  motors_speed(0.0, 0.0);
}


void loop() {
    Serial.print("left: ");
    Serial.print(" ");
    Serial.print(encoder_left());
    Serial.print(" ");
    Serial.print("right: ");
    Serial.println(encoder_right());


  delay(20);
}
