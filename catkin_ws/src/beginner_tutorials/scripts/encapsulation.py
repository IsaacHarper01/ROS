#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from math import pi, cos, sin
from geometry_msgs.msg import PointStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String

class Robot:
    def __init__(self):
        self.angle_rad = 0.0
        self.angle_grad = 0.0
        self.distance = 0.0
        self.laser_data = None
        self.odom_msg = None
        self.point = PointStamped()
        self.vel_msg = Twist()
        self.order = String()
        self.pub = rospy.Publisher("/speak",String,queue_size=1)
        sub = rospy.Subscriber("/scan", LaserScan, self.laser_callback)
        odom = rospy.Subscriber("/odom", Odometry,self.odom_callback)

    def laser_callback(self, data):
        self.laser_data = data

    def odom_callback(self,data):
        self.odom_msg = data

    def get_obstacle_point(self):
        if self.laser_data is None:
            return None
        max_distance = 100
        obstacle_angle = 0
        for i, distance in enumerate(self.laser_data.ranges):
            angle = self.laser_data.angle_min + i * self.laser_data.angle_increment
            if distance < max_distance:
                max_distance = distance
                obstacle_angle = angle
        self.angle_rad = obstacle_angle
        self.distance = max_distance
        self.pub.publish("i found the obstacle")
        return self.angle_rad, self.distance
    
    def get_euler_angle(self):
        self.angle_grad = (self.angle_rad * 180)/pi
        
    def get_point(self):
        self.point.header.frame_id = "rslidar"
        self.point.header.stamp = rospy.Time(0)
        self.point.point.x = self.distance * cos(self.angle_rad)
        self.point.point.y = self.distance * sin(self.angle_rad)
    
    def go_to_point(self):
        pub = rospy.Publisher("/cmd_vel", Twist,queue_size=1)
        self.vel_msg.angular.z = 0.75
        if self.vel_msg is None:  
            return None 
        pub.publish(self.vel_msg)
        

rospy.init_node("obstacle_detector")
robot = Robot()
rate = rospy.Rate(10) # 10 Hz

while not rospy.is_shutdown():
    robot.get_obstacle_point()
    #angle, distance = obstacle_point
    #robot.get_euler_angle()
    #robot.get_point()
    #robot.go_to_point()
    #print(robot.point)
    print("Obstacle detected at angle: {:.2f} radians, distance: {:.2f} m".format(robot.angle_rad, robot.distance))
    rate.sleep()

rospy.spin()