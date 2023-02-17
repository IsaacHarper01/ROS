import cv2 as cv
import numpy as np
from sklearn.linear_model import LinearRegression
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class Robot:
    def __init__(self):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.img_shape = []
        self.image = []
        self.slope = 0.0 
        self.pub_speak = rospy.Publisher("/speak",String,queue_size=1)
        self.pub_vel = rospy.Publisher("/cmd_vel",Twist,queue_size=1)

    def image_process(self,image):
        img = cv.imread(image)
        if img.shape[0] + img.shape[1] > 1050:
            factor = 0.3
            img = cv.resize(img,(int(img.shape[1]*factor),int(img.shape[0]*factor)),interpolation=cv.INTER_AREA)
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        blur = cv.blur(gray,(9,9))
        edges = cv.Canny(blur,150,150)
        self.img_shape = img.shape
        self.image = img
        return edges

    def line_detector(self,image): #requieres an edge image
        X1 = []
        Y1 = []
        lines = cv.HoughLinesP(image,1,np.pi/180,50)
        for line in lines:
            X1.append(line[0,0])
            X1.append(line[0,2])
            Y1.append(line[0,1])
            Y1.append(line[0,3])
        xnp = np.array(X1).reshape((-1,1))
        ynp = np.array(Y1)
        return xnp, ynp

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
        return x1, x2, y1, y2
    
    def get_line(self,image):
        edges = self.image_process(image)
        xnp, ynp = self.line_detector(edges)
        self.x1, self.x2, self.y1, self.y2 = self.linear_model(xnp,ynp)

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
robot.get_line("mps2.png")
cv.line(robot.image,(robot.x1,robot.y1),(robot.x2,robot.y2),(255,0,0), 4)
cv.imshow("IMAGE",robot.image)
print(robot.slope)
robot.alling(robot.slope)
cv.waitKey(30000)
cv.destroyAllWindows()
rospy.spin()