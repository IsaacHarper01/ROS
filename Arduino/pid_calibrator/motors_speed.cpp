#include <Arduino.h>

#define ML0  4
#define ML1 10
#define MR0  6
#define MR1  7

#define EL   5
#define ER  11


void set_motors(){
	pinMode(ML0, OUTPUT);
	pinMode(ML1, OUTPUT);
	pinMode(EL,  OUTPUT);
	pinMode(MR0, OUTPUT);
	pinMode(MR1, OUTPUT);
	pinMode(ER,  OUTPUT);
}

void move_motors(int left_dir, int left_pwm, int right_dir, int right_pwm) { 
		digitalWrite(ML0, !left_dir);
		digitalWrite(ML1, left_dir);
		analogWrite(EL, left_pwm);
        
		digitalWrite(MR0, right_dir);
		digitalWrite(MR1, !right_dir);
		analogWrite(ER, right_pwm);
}
