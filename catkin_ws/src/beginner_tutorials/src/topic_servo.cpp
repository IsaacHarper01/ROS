 #include "ros/ros.h"
 #include "std_msgs/UInt16.h"
 
 #include <sstream>

 int main(int argc, char **argv)
 {

   ros::init(argc, argv, "servo");

   ros::NodeHandle n;

   ros::Publisher chatter_pub = n.advertise<std_msgs::UInt16>("set_position_servo", 1000);
 
   ros::Rate loop_rate(20);

   int count = 0;
   while (ros::ok())
   {

     std_msgs::UInt16 msg;
     
     msg.data = count;

     chatter_pub.publish(msg);
 
     ros::spinOnce();
 
     loop_rate.sleep();

     if (count>=180){
      count=0;
     }
     ++count;
    
   }
 
 
   return 0;
 }
