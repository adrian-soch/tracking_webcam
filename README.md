# tracking_webcam

>A small project utilizing a servo to pan a webcam to follow a target.
Using rosserial to communicate from host computer to arduino. Arduino handles servo control.

Multiple tracking methods will be implemented, initially a colour based object detection will be deployed.

#### To-Do
- Use a different methodto get contours (ie canny edges)
- Implement a more robust tracking algorithm
- Update the algorithm for moving the servo towards the target (ie PID or something)
- 3D print a better servo/webcam base

#### Usage

Clone repository into catkin_ws/src
`cd ..` then `catkin_make`

`ls /dev/ | grep video` -> provides possible webcam indices
Ensure cv.VideoCapture(X) in tracking_webcam.py is using a valid argument

Upload the ros_servo_sub.ino to the arduino
Check `ls /dev/ttyACM*` to check which port the arduino is connected to
Ensure the tracking_webcam.launch has the correct port

Run `roslaunch tracking_webcam tracking_webcam.launch`

