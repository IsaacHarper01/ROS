#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from math import pi, cos, sin, atan2
from geometry_msgs.msg import PointStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion
import tf

class Robot:
    def __init__(self):
        self.angle_rad_lidar = 0.0
        self.angle_rad_odom = 0.0
        self.angle_grad = 0.0
        self.distance = 0.0
        self.laser_data = None
        self.odom_msg = Odometry()
        self.point_lidar = PointStamped()
        self.point_odom = PointStamped()
        self.vel_msg = Twist()
        self.order = String()
        self.pub = rospy.Publisher("/speak",String,queue_size=1)
        sub = rospy.Subscriber("/scan", LaserScan, self.laser_callback)
        odom = rospy.Subscriber("/odom", Odometry,self.odom_callback)

    def laser_callback(self, data):
        self.laser_data = data

    def odom_callback(self,data):
        self.odom_msg = data

    def get_obstacle_angle(self):
        while self.laser_data is None:
            continue
        max_distance = 100
        obstacle_angle = 0
        for i, distance in enumerate(self.laser_data.ranges):
            angle = self.laser_data.angle_min + i * self.laser_data.angle_increment
            if distance < max_distance:
                max_distance = distance
                obstacle_angle = angle
        self.angle_rad_lidar = obstacle_angle
        self.distance = max_distance
        self.pub.publish("i found the obstacle")
    
    def get_euler_angle(self):
        self.angle_grad = (self.angle_rad_lidar * 180)/pi
        
    def get_point_lidar(self):
        self.point_lidar.header.frame_id = "rslidar"
        self.point_lidar.header.stamp = rospy.Time(0)
        self.point_lidar.point.x = self.distance * cos(self.angle_rad_lidar)
        self.point_lidar.point.y = self.distance * sin(self.angle_rad_lidar)
    
    def go_to_point(self):
        pub = rospy.Publisher("/cmd_vel", Twist,queue_size=1)
        rot_q = self.odom_msg.pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
        errorx = self.point_odom.point.x - self.odom_msg.pose.pose.position.x 
        errory = self.point_odom.point.y - self.odom_msg.pose.pose.position.y
        angle_to_goal = atan2(errorx,errory)
        error_theta = angle_to_goal-theta
        direction = 0
        if error_theta < 0:
            direction = -1
        else:
            direction = 1
        print(error_theta)
        if abs(error_theta) <= 0.1:
            self.vel_msg.angular.z = 0.0
            self.vel_msg.linear.x = 0.5
        else:
            self.vel_msg.angular.z = 0.3 * direction
            self.vel_msg.linear.x = 0
        pub.publish(self.vel_msg)
        
    def get_point_odom(self):
        listener = tf.TransformListener()
        listener.waitForTransform("rslidar", "odom", rospy.Time(), rospy.Duration(4.0))
        listener.waitForTransform("rslidar", "odom",rospy.Time.now(), rospy.Duration(4.0))
        self.point_odom = listener.transformPoint('odom',self.point_lidar)
        print("odom point = ",self.point_odom)

rospy.init_node("obstacle_detector")
robot = Robot()
robot.get_obstacle_angle()
robot.get_point_lidar()
robot.get_point_odom()
robot.go_to_point()
# rate = rospy.Rate(10) # 10 Hz

# while not rospy.is_shutdown():
#     robot.go_to_point()
#     #print("Obstacle detected at angle: {:.2f} radians, distance: {:.2f} m".format(robot.angle_rad, robot.distance))
#     rate.sleep()

rospy.spin()