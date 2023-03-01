import cv2
import numpy as np

# read the image
img = cv2.imread('mps.jpg')
if img.shape[0] + img.shape[1] > 1050:
            factor = 0.2
            img = cv2.resize(img,(int(img.shape[1]*factor),int(img.shape[0]*factor)),interpolation=cv2.INTER_AREA)
# convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray,(2,2))
# apply Canny edge detection
edges = cv2.Canny(blur, 50, 150, apertureSize=3)

# perform Hough line transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100)

# filter the detected lines
filtered_lines = []
for line in lines:
    for x1, y1, x2, y2 in line:
        slope = (y2 - y1) / (x2 - x1)
        # filter out horizontal and vertical lines
        if abs(slope) < 0.5 or abs(slope) > 2:
            continue
        filtered_lines.append(line)

# calculate the slope of the remaining lines
slopes = []
for line in filtered_lines:
    for x1, y1, x2, y2 in line:
        slope = (y2 - y1) / (x2 - x1)
        slopes.append(slope)

# average the slopes to get the final slope of the table
avg_slope = sum(slopes) / len(slopes)

# calculate the y-intercept of the average line
y_intercept = img.shape[0] / 2

# calculate the x-intercept of the average line
x_intercept = int(y_intercept / avg_slope)

# draw the average line on the image
cv2.line(img, (0, y_intercept), (x_intercept, 0), (0, 255, 0), 4)

# display the image with the average line
cv2.imshow('image', img)
cv2.waitKey(15000)
cv2.destroyAllWindows()

