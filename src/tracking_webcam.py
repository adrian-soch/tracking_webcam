#!/usr/bin/env python

import cv2 as cv
import numpy as np
import sys
import rospy
from std_msgs.msg import UInt8
def servo_move_pub():

    pub = rospy.Publisher('servo', UInt8, queue_size=10)
    rospy.init_node('servo_move_pub', anonymous=False)
    rate = rospy.Rate(10) # Frequency in Hz

    cap = cv.VideoCapture(0) # Use 0 for built in webcam

    if not cap.isOpened():
        sys.exit()

    while not rospy.is_shutdown():

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

        low_red = np.array([0, 135, 122])
        high_red = np.array([255, 255, 255])
        red_mask = cv.inRange(hsv_frame, low_red, high_red)

        _, contours, _ = cv.findContours(red_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv.contourArea(x), reverse=True)

        for cont in contours:
            (x, y, w, h) = cv.boundingRect(cont)
            x_medium = int((x + x + w) / 2)
            #y_medium = int((y + y + h) / 2)
            #boxDim = [w, h]
            break

        cv.line(resized, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
        #cv.rectangle(resized, (x_medium - boxDim[0]/2, y_medium - boxDim[1]/2),(x_medium-boxDim[0]/2, y_medium + boxDim[1]/2), (x_medium + boxDim[0]/2, y_medium + boxDim[1]/2),(x_medium + boxDim[0]/2, y_medium - boxDim[1]/2), (0, 255, 0), 2)

        if x_medium < center -30:
            position = 80
        elif x_medium > center + 30:
            position = 100

        cv.line(resized, (x_medium, 0),(x_medium, 480), (0,255,0), 2)
        cv.imshow("Video", resized)

        key = cv.waitKey(1) 
        if  key == 27:
            cap.release()
            cv.destroyAllWindows
            break

        pub.publish(position)
        rate.sleep()

if __name__ == '__main__':
    try:
        servo_move_pub()
    except rospy.ROSInterruptException:
        pass
    