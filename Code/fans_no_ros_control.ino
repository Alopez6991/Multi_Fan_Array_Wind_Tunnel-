#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
int list[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35};
int FID[36][2] = {{0,0},{1,0},{2,0},{3,0},{4,0},{5,0},{6,0},{7,0},{8,0},{9,0},{10,0},{11,0},{12,0},{13,0},{14,0},{15,0},{16,0},{17,0},{18,0},{19,0},{20,0},{21,0},{22,0},{23,0},{24,0},{25,0},{26,0},{27,0},{28,0},{29,0},{30,0},{31,0},{32,0},{33,0},{34,0},{35,0}};
int r,a;
int Mode;
int Speed;
int Freq;
int new_info=0;
int toss[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35};
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x41);
Adafruit_PWMServoDriver pwm3 = Adafruit_PWMServoDriver(0x42);
void setup() {
Serial.begin(9600);
pwm1.begin();
  pwm1.setPWMFreq(100);  // 1600 is the max, use lower value to prevent "singing"
 
  pwm2.begin();
  pwm2.setPWMFreq(100);

  pwm3.begin();
  pwm3.setPWMFreq(100);

  randomSeed(analogRead(0));
}

void loop() {
  if (Serial.available()){
    Mode = Serial.read();
    new_info =0;
    }
//Mode='T';

if (Mode =='a' and new_info==0){
  Speed =32;
  for (int LAM=0; LAM<12; LAM++){

    pwm1.setPWM(LAM,0,Speed*40.95);
    pwm2.setPWM(LAM,0,Speed*40.95);
    pwm3.setPWM(LAM,0,Speed*40.95);
  }
new_info=1;     
}
if (Mode =='b' and new_info==0){
  Speed =20; 
  for (int LAM=0; LAM<12; LAM++){

    pwm1.setPWM(LAM,0,Speed*40.95);
    pwm2.setPWM(LAM,0,Speed*40.95);
    pwm3.setPWM(LAM,0,Speed*40.95);
  }
new_info=1;     
}

if (Mode =='L' and new_info==0){
  Speed =90;
  for (int LAM=0; LAM<12; LAM++){

    pwm1.setPWM(LAM,0,Speed*40.95);
    pwm2.setPWM(LAM,0,Speed*40.95);
    pwm3.setPWM(LAM,0,Speed*40.95);
  }
new_info=1;     
}

if (Mode =='B' and new_info==0){
  Speed =100;
    for (int i =0; i< 36; i++) {
//      toss[i]=random(0,2);
      
  
      if (FID[i][0] <=11) {pwm1.setPWM(FID[i][0],0,0.0);}
      else if ((FID[i][0] >=12) && (FID[i][0] <=17)) {pwm2.setPWM(FID[i][0]-12,0,0.0);}
      else if ((FID[i][0] >=18) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,Speed*40.95);}
      else if ((FID[i][0] >=24)) {pwm3.setPWM(FID[i][0]-24,0,Speed*40.95);}

  }
new_info=1;     
}

if (Mode =='U' and new_info==0){
  Speed =100;
    for (int i =0; i< 36; i++) {
//      toss[i]=random(0,2);
      
  
      if (FID[i][0] <=11) {pwm1.setPWM(FID[i][0],0,Speed*40.95);}
      else if ((FID[i][0] >=12) && (FID[i][0] <=17)) {pwm2.setPWM(FID[i][0]-12,0,Speed*40.95);}
      else if ((FID[i][0] >=18) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,0.0);}
      else if ((FID[i][0] >=24)) {pwm3.setPWM(FID[i][0]-24,0,0.0);}
  }
new_info=1;     
}

if (Mode =='z' and new_info==0){
  Serial.print(Mode);
  Speed =0;
  for (int LAM=0; LAM<12; LAM++){

    pwm1.setPWM(LAM,0,Speed*40.95);
    pwm2.setPWM(LAM,0,Speed*40.95);
    pwm3.setPWM(LAM,0,Speed*40.95);
  }
new_info=1;
}
if (Mode =='T' and new_info==0){
  Serial.print(Mode);
  Speed =100;

    for (int i =0; i< 36; i++) {
      toss[i]=random(0,2);
      
  
      if ((toss[i] == 0) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,Speed*40.95);}
      else if ((toss[i] == 0) && (FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,Speed*40.95);}
      else if ((toss[i] == 0) && (FID[i][0] >=24)) {pwm3.setPWM(FID[i][0]-24,0,Speed*40.95);}
      else if ((toss[i] == 1) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,0*40.95);}
      else if ((toss[i] == 1) &&(FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,0*40.95);}
      else if ((toss[i] == 1) && FID[i][0] >=24) {pwm3.setPWM(FID[i][0]-24,0,0*40.95);}
  }
  delay(1000);
//  new_info=1;

}
}
