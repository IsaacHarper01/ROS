#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point, PointStamped 
from nav_msgs.msg import Odometry
from math import sin, cos, atan2
import tf


goal= PointStamped()
angle_increment = 0.0
grad_angle = 0.0
angle = 0.0
actual_position = PointStamped()
actual = []
rot_q = []
theta = 0.0
theta_euler = 0.0
scan_data = []

#once we have calculated the distance and the angle of the obstacle we can get the exact point
# where the obstacle is
def get_point(angle,distance):
    global goal
    goal.point.x = distance * cos(angle-1.5707)
    goal.point.y = distance * sin(angle-1.5707)
    goal.header.stamp = rospy.Time(0)
    goal.header.frame_id = 'rslidar'
    #print(goal)

#recive and angle in radians and convert it into euler angles    
def get_angle(rad_angle):
    global grad_angle
    grad_angle = (180 * rad_angle )/3.1416
    return grad_angle

#this function recive the scan masures and calculate the distance to the obstacle
#return the indicator of the scan measure and the distance
def get_distance(scan):
    indicator=0
    distance_obs=100
    data_points = len(scan)
    for num in range(data_points):
        if (scan[num] != float('inf')):
            #print scan_data[num]
            if(distance_obs>scan[num]):
                distance_obs=scan[num]
                indicator = num
    return indicator, distance_obs

def callback(msg):
    global angle
    global scan_data
    global angle_increment
    scan_data = msg.ranges
    angle_increment = msg.angle_increment
    

def call_odom(msg_odom):
    global actual_position
    global actual
    global theta
    global theta_euler
    actual_position = msg_odom.pose.pose.position
    actual = msg_odom.pose.pose.orientation
    (roll, pitch, theta) = tf.transformations.euler_from_quaternion([actual.x,actual.y,actual.z,actual.w])
    theta_euler =  get_angle(theta)+90
    #print(theta_euler)

def husky_to_odom_frame(point):
    pub_point = rospy.Publisher('new_point',PointStamped,queue_size=1)
    new_point = PointStamped()
    listener = tf.TransformListener()
    listener.waitForTransform("rslidar", "odom",rospy.Time.now(), rospy.Duration(4.0))
    while not rospy.is_shutdown():
            now = rospy.Time.now()
            listener.waitForTransform("/rslidar", "/odom", now, rospy.Duration(4.0))
            new_point = listener.transformPoint('odom',point)
            pub_point.publish(new_point)

def control(actual_point,destination_point):
    error_x = 0.0
    error_y = 0.0
    error_x = destination_point.x - actual_point.x
    error_y = destination_point.y - actual_point.y 
    angle_error = atan2(error_y, error_x) 

rospy.init_node("laser_scan")
sub = rospy.Subscriber("/scan", LaserScan, callback)
sub_odom = rospy.Subscriber("/odom", Odometry, call_odom)
pub_point = rospy.Publisher("point_scan", PointStamped,queue_size=1)
while not rospy.is_shutdown():
    vector=[]
    vector = get_distance(scan_data)
    rad_angle = angle_increment*vector[0]
    angle = get_angle(rad_angle)
    get_point(rad_angle,vector[1])
    pub_point.publish(goal)
    #print(goal)
    #husky_to_odom_frame(goal)
rospy.spin()

