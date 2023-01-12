#include "encoders.h"
#include "motors_speed.h"

#define maxPID 20
#define minPID 0
#define maxPWM 255
#define minPWM 0

double vel = 0.15; 
int time = 180;
int foward   = HIGH;
int backward = LOW;

int left_pwm  = 0, right_pwm = 0;

double LKp = 0.6, LKi = 0.00051, LKd = 0.0013;
double RKp = 0.98, RKi = 0.0011, RKd = 0.0007;

double error_L, lastError_L, cumError_L, rateError_L;
double error_R, lastError_R, cumError_R, rateError_R;

float curr_speed_left = 0, curr_speed_right = 0;
float goal_speed_left = vel, goal_speed_right = vel;

float wheel_diameter = (43.38) / 1000;
unsigned int pulses_per_turn = 600;
unsigned long currentTime, previousTime;
volatile long rel_left_count = 0, rel_right_count = 0;
double elapsedTime, samplingTime = 40;

double samplingTimeSec = samplingTime / 1000.0;


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
/*
  Serial.print("left_pwm");
  Serial.print(" ");
  Serial.print(left_pwm);
  Serial.print(" ");
  Serial.print("right_pwm");
  Serial.print(" ");
  Serial.println(right_pwm);//*/
}

void pid(){
  currentTime = millis();
  elapsedTime = (double)(currentTime - previousTime);
  
  computeSpeeds();
  error_L = goal_speed_left  - curr_speed_left;
  error_R = goal_speed_right - curr_speed_right;
  
  cumError_L += error_L * elapsedTime;
  cumError_R += error_R * elapsedTime;
  
  rateError_L = (error_L - lastError_L) / samplingTimeSec;
  rateError_R = (error_R - lastError_R) / samplingTimeSec;

  double output_L = LKp*error_L + LKi*cumError_L + LKd*rateError_L;
  double output_R = RKp*error_R + RKi*cumError_R + RKd*rateError_R;
  
  lastError_L = error_L;
  lastError_R = error_R;

  speedsToPwm(output_L, output_R);
}

void setup() {
  set_motors();
  set_encoders_input();
  Serial.begin(230400);
  delay(1500);
  int i=0;

  while(i<time)
  {
    pid();
    move_motors(foward, left_pwm, foward, right_pwm);

    
    Serial.print("leftInput");
    Serial.print(" ");
    Serial.print(curr_speed_left*10);
    Serial.print(" ");
    
    Serial.print("rightInput");
    Serial.print(" ");
    Serial.print(curr_speed_right*10);
    Serial.print(" ");
    Serial.print("setPoint");
    Serial.print(" ");
    Serial.println(goal_speed_right*10);//*/
    
    i++;
    delay(20);
  }
  move_motors(foward, 0, foward, 0);
}

void loop() {
}
