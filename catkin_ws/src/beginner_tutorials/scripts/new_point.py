#!/usr/bin/env python

import rospy   
import tf
from geometry_msgs.msg import PointStamped 

point_get = PointStamped()

def husky_to_world(point):
    #pub_point = rospy.Publisher('new_point',PointStamped,queue_size=1)
    new_point = PointStamped()
    listener = tf.TransformListener()
    listener.waitForTransform("rslidar", "odom", rospy.Time(), rospy.Duration(4.0))
    listener.waitForTransform("rslidar", "odom",rospy.Time.now(), rospy.Duration(4.0))
    new_point = listener.transformPoint('odom',point)
    print(new_point)
    #pub_point.publish(new_point)

def call(msg):
    global point_get
    point_get = msg
    husky_to_world(point_get)

rospy.init_node('tf_convertion')
#sub = rospy.Subscriber("/point_scan", PointStamped, call)
rate = rospy.Rate(10)
point_get.header.frame_id="rslidar"
point_get.header.stamp = rospy.Time.now()
point_get.point.x= 3.68
point_get.point.y= 4.62
husky_to_world(point_get)
rate.sleep()
rospy.spin() 
    
    
    