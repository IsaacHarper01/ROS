#!/usr/bin/env python

from __future__ import division
import cv2 as cv
import numpy as np
from sklearn.linear_model import LinearRegression
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class Robot:
    def __init__(self):
        self.X1 = 0
        self.X2 = 0
        self.Y1 = 0
        self.Y2 = 0
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.img_shape = []
        self.image = None
        self.slopes= []
        self.slope = 0.0 
        self.b0=0.0
        self.pub_speak = rospy.Publisher("/speak",String,queue_size=1)
        self.pub_vel = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
        self.sub_img = rospy.Subscriber("/camera/rgb/image_color", Image, self.callback)

    def callback(self,data):
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(data, "bgr8")
        self.image = img
        self.get_line()
        cv.imshow("Kinect_image",img)
        cv.line(img,(self.x1,self.y1),(self.x2,self.y2),(255,0,0), 4)
        cv.line(img,(self.X1,self.Y1),(self.X2,self.Y2),(0,0,250), 4)
        cv.waitKey(1)

    def image_process(self):
        while self.image is None:
            continue
        img = self.image
        if img.shape[0] + img.shape[1] > 1200:
            factor = 0.2
            img = cv.resize(img,(int(img.shape[1]*factor),int(img.shape[0]*factor)),interpolation=cv.INTER_AREA)
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        blur = cv.blur(gray,(1,1))
        edges = cv.Canny(blur,150,150)
        self.img_shape = gray.shape
  
        #self.image = blur
        return edges
    
    def crop(self,img):
        crop_factor = 0.3
        heigth1 = (img.shape[0]/2) - (img.shape[0]*crop_factor)
        heigth2 = (img.shape[0]/2) + (img.shape[0]*crop_factor)
        width1 = (img.shape[1]/2) - (img.shape[1]*crop_factor)  
        width2 = (img.shape[1]/2) + (img.shape[1]*crop_factor) 
        crop_img = img[int(heigth1):int(heigth2), int(width1):int(width2)]
        return crop_img
    
    def line_detector(self,image): #requieres an edge image
        X1 = []
        Y1 = []
        lines = cv.HoughLinesP(image,1,np.pi/180,50)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2-y1)/(x2-x1)
            if slope < 0.15 and slope > -0.15:
                if slope == 0:
                    continue
                self.slopes.append(slope)
            if slope < 0.2 and slope > -0.2 :
                X1.append(x1)
                X1.append(x2)
                Y1.append(y1)
                Y1.append(y2)
                cv.line(self.image,(x1,y1),(x2,y2),(255,0,0), 4)
        xnp = np.array(X1).reshape((-1,1))
        ynp = np.array(Y1)
        return xnp, ynp
    
    def average_model(self):
        average = sum(self.slopes)/len(self.slopes)
        self.X1= 0
        self.X2 = self.img_shape[1]
        self.Y1 = int((average)*(self.X1)+self.b0)
        self.Y2 = int((average)*(self.X2)+self.b0)


    def linear_model(self, xnp, ynp):
        model = LinearRegression().fit(xnp,ynp)
        correlation = model.score(xnp,ynp)
        b0 = model.intercept_
        b1 = model.coef_
        x1 = 0
        x2 = self.img_shape[1]
        y1 = int((b1)*(x1)+b0)
        y2 = int((b1)*(x2)+b0)
        self.slope = b1
        self.b0 = b0
        return x1, x2, y1, y2
    
    def get_line(self):
        edges = self.image_process()
        xnp, ynp = self.line_detector(edges)
        self.x1, self.x2, self.y1, self.y2 = self.linear_model(xnp,ynp)
        self.average_model()

    def alling(self,slope):
        error = abs(slope)
        vel = Twist()
        while  error > 0.05:
            if slope < -0.05:
                vel.linear.y = 0.4
                vel.angular.z = 0.2
    
            if slope > 0.05:
                vel.linear.y = -0.4
                vel.angular.z= -0.2     
            self.pub_vel.publish(vel)
        vel.linear.x = 0
        vel.linear.y = 0
        vel.angular.z = 0
        self.pub_vel.publish(vel)
        return True

rospy.init_node("Alling")
robot = Robot()
#cv.line(robot.image_process(),(robot.x1,robot.y1),(robot.x2,robot.y2),(255,0,0), 4)
# cv.line(robot.image,(robot.X1,robot.Y1),(robot.X2,robot.Y2),(0,255,0), 4)
# #robot.alling(robot.slope)
rospy.spin()