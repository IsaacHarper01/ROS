#!/usr/bin/env python
import rospy 
from sensor_msgs.msg import PointCloud2

def callback(cloud):
    field = cloud.fields
    data = cloud.data
    print ("data")
    print (len(data))
   
    print ("field")
    print (len(field), field)

rospy.init_node("point_sub")
sub = rospy.Subscriber("/rslidar_points",PointCloud2,callback)
rospy.spin()