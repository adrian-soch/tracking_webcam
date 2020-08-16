
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
#include <std_msgs/Int16.h>

int laserPin = 8;
int speedDesired = 0;


AccelStepper stepper; // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
ros::NodeHandle  nh;

void stepper_cb( const std_msgs::Int16 & cmd_msg){
   stepper.setSpeed(cmd_msg.data);
   if(cmd_msg.data != 0){
    digitalWrite(laserPin, HIGH);
   }
   else
    digitalWrite(laserPin, LOW);
  
}

ros::Subscriber<std_msgs::Int16> sub("stepper", stepper_cb);

void setup()
{  
  pinMode(laserPin, OUTPUT);
  stepper.setMaxSpeed(1200);
  
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{   
   stepper.runSpeed();
   nh.spinOnce();
   delay(1);
}
