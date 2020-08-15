# tracking_webcam

![IMG_0379](https://user-images.githubusercontent.com/6884645/87463069-d8dd1300-c5de-11ea-9487-db58ed457b65.jpg)

##### A small project utilizing computer vision to follow a target with a webcam in the horizontal plane.

Using rosserial to communicate from host computer to arduino. Arduino handles servo/stepper control.

Current tracking method is based on HSV colour detection.

#### Hardware
- Base and webcam holder (STL models [here](https://github.com/adrian-soch/tracking_webcam/tree/master/stl))
- Any arduino or arduino clone
- USB 2.0 Cable Type A/B
- Servo motor
- USB Webcam
- Stepper Motor + Driver (28BYJ-48)

#### To-Do
- Implement a deep learning tracking model
- Investigate Kalman filter for tracking stability
- Update the algorithm for moving the servo towards the target (ie PID or something)
- ~~3D print a better servo/webcam base~~

#### Usage

Clone repository into catkin_ws/src,
`cd ..` then `catkin_make`

`ls /dev/ | grep video` -> provides possible webcam indices
Ensure cv.VideoCapture(X) in tracking_webcam.py is using a valid argument

Upload the ros_servo_sub.ino to the arduino
Check `ls /dev/ttyACM*` to check which port the arduino is connected to
Ensure the tracking_webcam.launch has the correct port

Run `roslaunch tracking_webcam servo.launch` or `roslaunch tracking_webcam stepper.launch`

#### Notes

Run `include/range-detector.py --filter HSV --webcam` to see a live preview with the HSV mask, you can adjust the sliders for any colour you want to detect. This can also be a convenient place to test any other algorithms for segmentation.

> WSL 2 does not yet support using the webcam or usb ports, I did not check if this works on a VM, nor did I check if this works with the Windows installation of ROS
