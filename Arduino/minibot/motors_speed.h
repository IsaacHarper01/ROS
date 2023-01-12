void set_motors(float left_pid1[3], float left_pid2[3], float right_pid1[3], float right_pid2[3]);
void computeSpeeds();
volatile long encoder_left();
volatile long encoder_right();
void speedsToPwm(double output_L, double output_R);
void motors_speed(float goal_speed_left, float goal_speed_right);
