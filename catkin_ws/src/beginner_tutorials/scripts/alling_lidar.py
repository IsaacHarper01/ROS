#!/usr/bin/env python

from __future__ import division
import rospy 
from sensor_msgs.msg import LaserScan, PointCloud2
import statistics 
import sensor_msgs.point_cloud2 as pc2

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

class LidarConverter:
    def __init__(self):
        self.cloud_sub = rospy.Subscriber('/camera/depth/points', PointCloud2, self.convert_cloud)
        self.lidar_pub = rospy.Publisher('/lidar_topic', LaserScan, queue_size=10)

    def convert_cloud(self, msg):
        scan = LaserScan()
        scan.header = msg.header
        scan.angle_min = -3.14159
        scan.angle_max = 3.14159
        scan.angle_increment = 0.01745
        scan.time_increment = 0.0
        scan.scan_time = 0.1
        scan.range_min = 0.0
        scan.range_max = 100.0
        scan.ranges = []
        scan.intensities = []

        for point in pc2.read_points(msg, skip_nans=True):
            scan.ranges.append(point[2])
            scan.intensities.append(point[3])

        self.lidar_pub.publish(scan)
    
rospy.init_node("alling")
lc = LidarConverter()
#robot = robot()
#print(robot.comp())
rospy.spin()
