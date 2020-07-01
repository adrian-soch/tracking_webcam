#!/usr/bin/env python

import cv2 as cv
import numpy as np
import sys
import rospy
from std_msgs.msg import UInt8

cap = cv.VideoCapture(4) # Use 0 for built in webcam

if not cap.isOpened():
    sys.exit()

 

while True:
    ok, frame = cap.read()

    scale_percent = 100 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv.resize(frame, dim, interpolation = cv.INTER_AREA) 

    rows, cols, _ = resized.shape
    x_medium = int(cols / 2)
    center = int(cols / 2)

    position = 90
    hsv_frame = cv.cvtColor(resized, cv.COLOR_BGR2HSV)

    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv.inRange(hsv_frame, low_red, high_red)

    _, contours, _ = cv.findContours(red_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv.contourArea(x), reverse=True)

 

    for cont in contours:
        (x, y, w, h) = cv.boundingRect(cont)
        x_medium = int((x + x + w) / 2)
        break

    cv.line(resized, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)

    if x_medium < center -30:
        position += 1
    elif x_medium > center + 30:
        position -= 1

    cv.imshow("Video", resized)

    cv.line(resized, (x_medium, 0),(x_medium, 480), (0,255,0), 2)

    key = cv.waitKey(1) 

    if  key == 27:
        cap.release()
        cv.destroyAllWindows
        break
    