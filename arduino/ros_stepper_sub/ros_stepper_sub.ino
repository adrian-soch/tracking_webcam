
/*
 * Author: Adrian Sochaniwsky
 */
 
#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <AccelStepper.h>
#include <ros.h>
#include <std_msgs/UInt8.h>

int laserPin = 8;

AccelStepper stepper; // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
ros::NodeHandle  nh;

void stepper_cb( const std_msgs::UInt8 & cmd_msg){
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  if(cmd_msg.data != 0)
    digitalWrite(laserPin, LOW);  //laser off when stationary 
   else
    digitalWrite(laserPin, HIGH);  //laser on when moving 
}

ros::Subscriber<std_msgs::UInt8> sub("stepper", stepper_cb);

void setup()
{  
  pinMode(laserPin, OUTPUT);
  
  stepper.setMaxSpeed(1000);
  //stepper.setSpeed(50);	
  
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{  
   //stepper.runSpeed();
   nh.spinOnce();
   delay(1);
}
