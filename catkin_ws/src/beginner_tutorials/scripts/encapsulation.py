#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

class Robot:
    def __init__(self):
        self.angle = 0.0
        self.distance = 0.0
        self.laser_data = None
        sub = rospy.Subscriber("/scan", LaserScan, self.laser_callback)

    def laser_callback(self, data):
        self.laser_data = data

    def get_obstacle_point(self):
        if self.laser_data is None:
            return None
        max_distance = -1
        obstacle_angle = 0
        for i, distance in enumerate(self.laser_data.ranges):
            angle = self.laser_data.angle_min + i * self.laser_data.angle_increment
            if distance > max_distance:
                max_distance = distance
                obstacle_angle = angle

        self.angle = obstacle_angle
        self.distance = max_distance
        return self.angle, self.distance

rospy.init_node("obstacle_detector")
robot = Robot()
rate = rospy.Rate(10) # 10 Hz

while not rospy.is_shutdown():
    obstacle_point = robot.get_obstacle_point()
    print(obstacle_point)
    if obstacle_point is not None:
        angle, distance = obstacle_point
        print("Obstacle detected at angle: {:.2f} radians, distance: {:.2f} m".format(robot.angle, robot.distance))
    rate.sleep()

rospy.spin()