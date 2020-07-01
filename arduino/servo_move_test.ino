#include <Servo.h> 

int laserPin = 8;
Servo servo;
int pos = 90;
int temp = 90;

void update(int pos){
  servo.write(pos); //set servo angle, should be from 0-180  
  if(pos == 90)
    digitalWrite(laserPin, LOW);  //laser off when stationary 
   else
    digitalWrite(laserPin, HIGH);  //laser on when moving 
}



void setup(){
  Serial.begin(9600);
  Serial.print("Enter Position = ");
  pinMode(laserPin, OUTPUT);
  servo.attach(9); //use pin 9 to control servo
}

void loop(){
  if(Serial.available()>0)
    { 
    temp = Serial.parseInt();   
    if(temp >=1 )
      pos = temp;
      Serial.print(pos);  
      Serial.println(" degree");
      Serial.print("Enter Position = ");
      update(pos);
    }
    delay(15);
}
