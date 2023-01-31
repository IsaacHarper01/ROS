#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped 
from math import sin, cos


class Robot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.angle_obs = 0.0
        self.distance_obs= 0.0
        self.laser_data = []
        sub_scan = rospy.Subscriber("/scan",LaserScan,self.laser_callback)

    def laser_callback(self, data):
        self.laser_data = data
        print(self.laser_data)

    def get_dist_angle(self):
        data = self.laser_data
        angle = 0.0
        aux = 0.0
        print(data)   
        for i in range(len(data.ranges)):
            angle = data.angle_min + i * data.angle_increment
            distance_obs = data.ranges[i]
            if data.ranges[i] == float('Inf') or data.ranges[i] == float('NaN'):
                continue
            if(distance_obs > aux):
                aux = distance_obs
                angle_max = angle
        return angle_max, aux
        
        
    def get_point(self, angle, distance):
        x = distance * cos(angle)
        y = distance * sin(angle)
        point = PointStamped()
        point.point.x = x
        point.point.y = y 
        point.header.frame_id = "rslidar"
        point.header.stamp = rospy.Time(0)
        return point


rospy.init_node("laser_odom")
husky = Robot("husky")
while not rospy.is_shutdown():
    obs_point = husky.get_dist_angle()
    print(obs_point)
rospy.spin()