#!/usr/bin/env python

import rospy   
import tf
from geometry_msgs.msg import PointStamped 

point_get = PointStamped()

def husky_to_world(point):
    pub_point = rospy.Publisher('new_point',PointStamped,queue_size=1)
    new_point = PointStamped()
    listener = tf.TransformListener()
    listener.waitForTransform("rslidar", "odom", rospy.Time.now(), rospy.Duration(4.0))
    while not rospy.is_shutdown():
            now = rospy.Time.now()
            listener.waitForTransform("rslidar", "odom", now, rospy.Duration(4.0))
            new_point = listener.transformPoint('odom',point)
            pub_point.publish(new_point)

def call(msg):
    global point_get
    point_get = msg

rospy.init_node('tf_convertion')
sub = rospy.Subscriber("/point_scan", PointStamped,call)
husky_to_world(point_get)