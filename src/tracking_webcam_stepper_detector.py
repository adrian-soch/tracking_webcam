#!/usr/bin/env python

import cv2 as cv
import numpy as np
import argparse
import sys
import rospy
from std_msgs.msg import Int16

print(cv.__version__)



def servo_move_pub():
    freq = 30

    pub = rospy.Publisher('stepper', Int16, queue_size=10)
    rospy.init_node('stepper_move_pub', anonymous=False)
    rate = rospy.Rate(freq) # Frequency in Hz



    thresh = 0.6
    prototxt = "MobileNetSSD_deploy.prototxt.txt"
    model = "MobileNetSSD_deploy.caffemodel"
    dir = rospy.get_param("~data_dir")


    # Shortened List
    classNames = { 0: 'background',
        1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
        5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
        10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
        14: 'motorbike', 15: 'person', 16: 'pottedplant'}

    net = cv.dnn.readNetFromCaffe(dir + prototxt, dir + model)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)




    cap = cv.VideoCapture(2) # Use 0 for built in webcam

    if not cap.isOpened():
        cap.release()
        sys.exit()

    speed = 0
    k_p = 2
    deadzone = 30
    center_x = 150

    while not rospy.is_shutdown():

        timer = cv.getTickCount()

        ret, frame = cap.read()
        frame_resized = cv.resize(frame,(300,300))
        
        rows, cols, _ = frame_resized.shape
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > thresh:
                class_id = int(detections[0, 0, i, 1])

                xLeftBottom = int(detections[0, 0, i, 3] * cols)
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)

                heightFactor = frame.shape[0]/300.0
                widthFactor = frame.shape[1]/300.0
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom)
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object
                cv.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),(0, 255, 0))
                # Find center of detection
                center_x = int((xLeftBottom + xRightTop)/2.0)

                if class_id in classNames:

                    label = classNames[class_id] + ": " + "{:2.3f}".format(confidence) #f'{confidence:.3}'
                    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]), (xLeftBottom + labelSize[0], yLeftBottom + baseLine),(255, 255, 255), cv.FILLED)
                    cv.putText(frame, label, (xLeftBottom, yLeftBottom),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                    label = "fps: " + "{:.1f}".format(fps)#f'{fps:.3}'
                    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv.rectangle(frame, (0, 15 - labelSize[1]), (0 + labelSize[0], 15 + baseLine),(255, 255, 255), cv.FILLED)
                    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (20, 20, 255))

        # Determining Motor Speeds
        err = center - center_x
        
        if(abs(err) > deadzone):
            speed = err*k_p
        else:
            speed = 0

        cv.namedWindow("frame", cv.WINDOW_AUTOSIZE)
        cv.imshow("Object Detector", frame)

        key = cv.waitKey(1) 
        if  key == 27:
            cap.release()
            cv.destroyAllWindows
            break

        #rospy.loginfo("Error: %d\nspeed: %d", err, speed)
        pub.publish(speed)
        rate.sleep()

if __name__ == '__main__':
    try:
        servo_move_pub()
    except rospy.ROSInterruptException:
        pass
    
