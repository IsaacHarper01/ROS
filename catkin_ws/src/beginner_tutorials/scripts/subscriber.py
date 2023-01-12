#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan


def callback(msg):
    comp = 0.0
    indicator = 0
    scan_data = msg.ranges
    index = len(scan_data)
    for num in range(index):
        if (scan_data[num] != float('inf')):
            #print scan_data[num]
            if(scan_data[num]>=comp):
                comp=scan_data[num]
                indicator = num
    print(comp,indicator)

rospy.init_node("laser_scan")
sub = rospy.Subscriber("/scan", LaserScan, callback)
rospy.spin()