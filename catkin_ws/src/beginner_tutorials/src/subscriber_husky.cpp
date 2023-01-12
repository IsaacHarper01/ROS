#include "ros/ros.h"
#include "std_msgs/Float32.h"
#include "sensor_msgs/LaserScan.h"

void callback(const sensor_msgs::LaserScan& msg){
    ROS_INFO("I heard: [%f]", msg.intensities);

}

int main(int argc, char **argv){

ros::init(argc, argv, "scan_subscriber");
ros::NodeHandle nh;
ros::Subscriber scan_sub = nh.subscribe("/scan",1000,callback);
ros::spin();
return 0;

}