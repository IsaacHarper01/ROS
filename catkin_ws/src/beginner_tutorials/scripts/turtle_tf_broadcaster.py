#!/usr/bin/env python  
import rospy   
import tf

def pub_tf():
    br = tf.TransformBroadcaster()
    while not rospy.is_shutdown():
        br.sendTransform((2.0, 3.0, 0.0),(0.0, 0.0, 0.0, 1.0),rospy.Time.now(),'husky','world')        


rospy.init_node('turtle_tf_broadcaster')
pub_tf()
rospy.spin()