import cv2
import numpy as np

# (1) read into  bgr-space
img = cv2.imread("test2.jpg")

# (2) convert to hsv-space, then split the channels
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)

# (3) threshold the S channel using adaptive method(`THRESH_OTSU`) or fixed thresh
th, threshed = cv2.threshold(s, 50, 255, cv2.THRESH_BINARY_INV)

# (4) find all the external contours on the threshed S
cnts = cv2.findContours(threshed, cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
canvas = img.copy()
#cv2.drawContours(canvas, cnts, -1, (0,255,0), 1)

# sort and choose the largest contour
cnts = sorted(cnts, key=cv2.contourArea)
cnt = cnts[-1]

# approx the contour, so the get the corner points
arclen = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.02 * arclen, True)
cv2.drawContours(canvas, [cnt], -1, (255, 0, 0), 1, cv2.LINE_AA)
cv2.drawContours(canvas, [approx], -1, (0, 0, 255), 1, cv2.LINE_AA)

# Ok, you can see the result as tag(6)
cv2.imwrite("detected.png", canvas)
