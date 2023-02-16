import cv2 as cv
import numpy as np

img = cv.imread("MPS.jpg")
imgre = cv.resize(img,(630,420),interpolation=cv.INTER_AREA)
gray = cv.cvtColor(imgre,cv.COLOR_BGR2GRAY)
blur = cv.blur(gray,(7,7))
edges = cv.Canny(blur,150,150)
 
lines = cv.HoughLinesP(edges,1,np.pi/180,50)
print(lines.shape)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(blur,(x1,y1),(x2,y2),(255,0,0), 4)



cv.imshow("IMAGE", blur)
#cv.imshow("canny",edges)
cv.waitKey(10000)
cv.destroyAllWindows()
