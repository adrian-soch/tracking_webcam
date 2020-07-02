# tracking_webcam

> A small project utilizing computer vision to follow a target with a webcam in the horizontal plane.

Using rosserial to communicate from host computer to arduino. Arduino handles servo control.

Current tracking method is based on HSV colour detection.

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

#### Notes

Run `include/range-detector.py --filter HSV --webcam` to see a live preview with the HSV mask, you can adjust the sliders for any colour you want to detect.

> WSL 2 does not yet support using the webcam or usb ports, I did not check if this works on a VM, nor did I check if this works with the Windows installation of ROS
