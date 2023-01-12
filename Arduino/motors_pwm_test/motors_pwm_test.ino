#include "motors_pwm.h"

int foward = 1, backward = 0;
int left_pwm = 0, right_pwm = 0;

void setup()
{
    set_motors_output();
}

void loop()
{
    motors_pwm(foward, left_pwm, foward, right_pwm);
    delay(20);
}
