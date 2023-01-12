#include "sensors.h"

int* line_sensor;
int* light_sensor;
int* sharp_sensor;
int battery_sensor;

void setup() {

	Serial.begin(9600);
	set_line_sensors();
}

void loop() {
	
	read_sensors_data();
	
	light_sensor = get_light_sensors();
	Serial.print("[");
        Serial.print(light_sensor[0]);
	for(int i=1; i<8; i++)
	{
	  Serial.print(", ");
          Serial.print(light_sensor[i]);
	}
	Serial.print("]\t");//*/

	sharp_sensor = get_sharp_sensors();
	Serial.print("[");
        Serial.print(sharp_sensor[0]);
	for(int i=1; i<7; i++)
	{
	  Serial.print(", ");
          Serial.print(sharp_sensor[i]);
	}
	Serial.print("]\t");//*/

	battery_sensor = get_battery_sensor();
	Serial.print("[");
	Serial.print(battery_sensor);
	Serial.print("]\t");
	
	line_sensor = get_line_sensors();
	Serial.print("[");
	Serial.print(line_sensor[0]);
	Serial.print(", ");
	Serial.print(line_sensor[1]);
	Serial.println("]\t");
	
	delay(200);	
}
