#!/usr/bin/env python

from __future__ import division
import rospy 
from sensor_msgs.msg import LaserScan
import statistics 

class robot:
    def __init__(self):
        self.data = None
        self.scan_sub = rospy.Subscriber("/scan",LaserScan,self.laser_callback)

    def laser_callback(self,data):
        self.data = data

    def comp(self):
        ranges = []
        while self.data is None:
            continue
        for i, distance in enumerate(self.data.ranges):
            angle = self.data.angle_min + i * self.data.angle_increment
            if distance < 2:
                distance = round(distance,1)
                ranges.append(distance)
        mode =  statistics.mode(ranges)
        print(mode)
        average = sum(ranges)/len(ranges)
        error_line = mode - average
        if abs(error_line) > 0.03:
            print(error_line)
            return False
        else:
            print(error_line)
            return True

rospy.init_node("alling")
robot = robot()
print(robot.comp())
rospy.spin()
