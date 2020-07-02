/*
 * Using Base code from: rosserial Servo Control Example
 * Using Laser module instead of built in LED
 * Swapped move_servo message type from Uint16 -> Uint8
 */

#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt8.h> // 0 - 255 values accepted

int laserPin = 8;

ros::NodeHandle  nh;

Servo servo;

void servo_cb( const std_msgs::UInt8 & cmd_msg){
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  if(cmd_msg.data == 90)
    digitalWrite(laserPin, LOW);  //laser off when stationary 
   else
    digitalWrite(laserPin, HIGH);  //laser on when moving 
}


ros::Subscriber<std_msgs::UInt8> sub("servo", servo_cb);

void setup(){
  pinMode(laserPin, OUTPUT);
  
  //nh.getHardware()->setBaud(115200);
  
  nh.initNode();
  nh.subscribe(sub);
  
  //Serial.begin(115200);
  servo.attach(9); //use pin 9 to control servo
}

void loop(){
  nh.spinOnce();
  delay(2);
}
