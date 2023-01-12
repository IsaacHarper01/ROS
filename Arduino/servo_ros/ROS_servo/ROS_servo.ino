#include<ros.h>
#include<std_msgs/UInt16.h>
#include<Servo.h>

ros::NodeHandle nh;
Servo servo;

void servo_action(const std_msgs::UInt16& angle)
{
      servo.write(angle.data);
}

std_msgs::UInt16 get_position;
ros::Publisher pub_position("get_position_servo", &get_position);
ros::Subscriber<std_msgs::UInt16> sub_position("set_position_servo", servo_action);


int valor;



void setup() 
{
    nh.initNode();  
    nh.advertise(pub_position);
    nh.subscribe(sub_position);
}

void loop() 
{
 servo.attach(9);
 valor = servo.read();
 get_position.data = valor;
 pub_position.publish(&get_position);
 nh.spinOnce();
 delay(100);
}
