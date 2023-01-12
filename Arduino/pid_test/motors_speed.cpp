#include <Arduino.h>
#include "encoders.h"
#include "motors_pwm.h"

#define maxPID 20
#define minPID 0
#define maxPWM 255
#define minPWM 0


int leftFoward = HIGH, rightFoward = HIGH;

double LKp = 0.6, LKi = 0.00051, LKd = 0.0013;
double RKp = 0.98, RKi = 0.0011, RKd = 0.0007;

double error_L, lastError_L, cumError_L, rateError_L;
double error_R, lastError_R, cumError_R, rateError_R;

int left_pwm  = 0, right_pwm = 0;
float curr_speed_left = 0, curr_speed_right = 0;

float wheel_diameter = (43.38) / 1000;
unsigned int pulses_per_turn = 600;

unsigned long currentTime, previousTime;
volatile long rel_left_count = 0, rel_right_count = 0;
double elapsedTime, samplingTime = 40;

double samplingTimeSec = samplingTime / 1000.0;

void set_motors()
{
  set_motors_output();
  set_encoders_input();
}

volatile long encoder_left()
{
  return left_count();
}
volatile long encoder_right()
{
  return right_count();
}

void computeSpeeds()
{
  if (elapsedTime >= samplingTime)
  {
    rel_left_count  = left_count()  - rel_left_count;
    rel_right_count = right_count() - rel_right_count;
    
    curr_speed_left  = 3.1416 * wheel_diameter * fabs(rel_left_count)  / pulses_per_turn * 1000.0 / elapsedTime;
    curr_speed_right = 3.1416 * wheel_diameter * fabs(rel_right_count) / pulses_per_turn * 1000.0 / elapsedTime;

    rel_left_count  = left_count();
    rel_right_count = right_count();
    previousTime = currentTime;
  }
}

void speedsToPwm(double output_L, double output_R)
{
  left_pwm  = map(output_L*100, minPID, maxPID, minPWM, maxPWM);
  right_pwm = map(output_R*100, minPID, maxPID, minPWM, maxPWM); 

  if(left_pwm  < 0)  left_pwm = 0;
  if(right_pwm < 0) right_pwm = 0;  

  if(left_pwm  > 255)  left_pwm = 255;
  if(right_pwm > 255) right_pwm = 255;
}

void motors_speed(float goal_speed_left, float goal_speed_right){
  currentTime = millis();
  elapsedTime = (double)(currentTime - previousTime);
  
  computeSpeeds();
  error_L = fabs(goal_speed_left) - curr_speed_left;
  error_R = fabs(goal_speed_right) - curr_speed_right;
  
  cumError_L += error_L * elapsedTime;
  cumError_R += error_R * elapsedTime;
  
  rateError_L = (error_L - lastError_L) / samplingTimeSec;
  rateError_R = (error_R - lastError_R) / samplingTimeSec;

  double output_L = LKp*error_L + LKi*cumError_L + LKd*rateError_L;
  double output_R = RKp*error_R + RKi*cumError_R + RKd*rateError_R;
  
  lastError_L = error_L;
  lastError_R = error_R;

  speedsToPwm(output_L, output_R);
  if(goal_speed_left  < 0) leftFoward  = LOW;
  if(goal_speed_right < 0) rightFoward = LOW;

  if(goal_speed_left  == 0) left_pwm  = 0;
  if(goal_speed_right == 0) right_pwm = 0;

  motors_pwm(leftFoward, left_pwm, rightFoward, right_pwm);
}
