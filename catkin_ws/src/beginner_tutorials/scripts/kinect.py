#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def callback(data):
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("Image window", img)
    cv2.waitKey(1)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/camera/rgb/image_color", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
