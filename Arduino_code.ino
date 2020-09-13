#include <Servo.h>
//defining variables
#define ir 4
#define buzzer 8
#define led 7
#define ldr A0
int i_r=0;
int angle=120;
Servo servom;
void setup() {
  //describing pinmodes of all the pins
  Serial.begin(9600);
  pinMode(ir,INPUT);
  pinMode(led,OUTPUT);
  pinMode(ldr,INPUT);
  pinMode(buzzer,OUTPUT);
  servom.attach(11);
  servom.write(angle);
}

void condition(int i_r,int l_d_r){
  int sth=0;
  if(i_r==0 && l_d_r >=800){	//6.condition for opening motor
      
//7.instructions for motor functioning based on our application.
for(angle=120;angle<=0;angle-=1){	
          servom.write(angle);
          delay(10);}
      for(angle=0;angle<=120;angle+=1){
          servom.write(angle);
          delay(10);}
          sth=11;
          delay(500);
          Serial.println(sth);}
    else if(i_r==0 && l_d_r<700){	//8.condition for activating Buzzer.which means thrown one is not a bottle.
      Serial.println(2);
      digitalWrite(buzzer,HIGH);
      delay(1000);
      digitalWrite(buzzer,LOW);
    }
    else{
	//9.data sending through USB port which is accessed in python code.
      Serial.println(2);
    }
}
void func(){				//2.IR sensor detects object.
   i_r=digitalRead(ir);
   if(i_r==0){			//3.if object is there led will be turned ON
     digitalWrite(led,HIGH);
   }
   else{				//4.else,led will be remained OFF
     digitalWrite(led,LOW);
   }
   delay(1000);
   int l_d_r=analogRead(ldr);
   condition(i_r,l_d_r);	//5.condition function is called with parameters of ir,ldr sensor values.
}
void loop(){
  while(Serial.available()>0){//1.if arduino gets data function will be called
  func();
  break;
  }
  //below code is for functioning the machine without taking any data from the user as he/she is not interested for money. 
  if(Serial.available()==0){
    i_r=digitalRead(ir);
    if(i_r==0){
       digitalWrite(led,HIGH);
     }
    else{
       digitalWrite(led,LOW);
    }
    delay(1000);
    int l_d_r=analogRead(ldr);
    if(i_r==0 && l_d_r >=800){
      for(angle=120;angle<=0;angle-=1){
          servom.write(angle);
          delay(10);}
      for(angle=0;angle<=120;angle+=1){
          servom.write(angle);
          delay(10);}
          }
     else if(i_r==0 && l_d_r<700){
      digitalWrite(buzzer,HIGH);
      delay(1000);
      digitalWrite(buzzer,LOW);
     }
  delay(2000);
}
}
