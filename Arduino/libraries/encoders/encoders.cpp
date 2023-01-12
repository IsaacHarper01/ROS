#include <Arduino.h>

#define RH_ENCODER_A 2
#define RH_ENCODER_B 8
#define LH_ENCODER_A 3
#define LH_ENCODER_B 9

volatile  long rightCount = 0;
volatile  long leftCount = 0;


void leftEncoderEvent(){
  if(digitalRead(LH_ENCODER_A) == HIGH)
    if(digitalRead(LH_ENCODER_B) == LOW) leftCount--;
    else leftCount++;
  else
    if(digitalRead(LH_ENCODER_B) == LOW) leftCount++;
    else leftCount--;
}

void rightEncoderEvent(){
  if(digitalRead(RH_ENCODER_A) == HIGH)
    if(digitalRead(RH_ENCODER_B) == LOW) rightCount++;
    else rightCount--;
  else
    if(digitalRead(RH_ENCODER_B) == LOW) rightCount--;
    else rightCount++;
}

volatile long left_count(){
	return leftCount;
}

volatile long right_count(){
	return rightCount;
}

void set_encoders_input(){
	pinMode(RH_ENCODER_A, INPUT);
	pinMode(RH_ENCODER_B, INPUT);
	pinMode(LH_ENCODER_A, INPUT);
	pinMode(LH_ENCODER_B, INPUT);

	attachInterrupt(0, rightEncoderEvent, CHANGE);
	attachInterrupt(1, leftEncoderEvent, CHANGE);
}
