#include "Arduino.h"

#define R_LSENSOR 12
#define L_LSENSOR 13

int ldr[8];
int sharp[8];
int line[2];
int battery;

void set_line_sensors() {
    pinMode(R_LSENSOR, INPUT);
    pinMode(L_LSENSOR, INPUT);
}

void read_sensors_data() {

    for(int i=0; i<8; i++)
        ldr[i] = analogRead(i);

    for(int i=8; i<15; i++)
	sharp[i-8] = analogRead(i);
    
    battery = analogRead(15);
    line[0] = digitalRead(R_LSENSOR);    
    line[1] = digitalRead(L_LSENSOR);
}

int get_battery_sensor(){
    return battery;
}

int* get_light_sensors(){
    return ldr;
}

int* get_sharp_sensors(){
    return sharp;
}

int* get_line_sensors() {
    return line; 
}
