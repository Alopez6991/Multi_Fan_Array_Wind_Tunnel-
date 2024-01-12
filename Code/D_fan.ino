#include <ros.h>
#include <std_msgs/UInt32MultiArray.h>
#include <std_msgs/UInt16MultiArray.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
ros::NodeHandle nh;
float t, s1, s2, s3, s, S, TI, T2, DT,F,FF,FFF;

float p[10];
float Si[36];
float TT[36];
int FID[36][2] = {{0,0},{1,0},{2,0},{3,0},{4,0},{5,0},{6,0},{7,0},{8,0},{9,0},{10,0},{11,0},{12,0},{13,0},{14,0},{15,0},{16,0},{17,0},{18,0},{19,0},{20,0},{21,0},{22,0},{23,0},{24,0},{25,0},{26,0},{27,0},{28,0},{29,0},{30,0},{31,0},{32,0},{33,0},{34,0},{35,0}};
int count = 36;
int numbers[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35};
int r,a;
int Mode;
int Speed;
int Freq;
int RPM[36];
int coin;
int list[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35};
int toss[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35};
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x41);
Adafruit_PWMServoDriver pwm3 = Adafruit_PWMServoDriver(0x42);
//int FAN[3];
//int order[36];

void messageCb(const std_msgs::UInt32MultiArray& cdm_msg)
{
cdm_msg.data;

//Serial.write(cdm_msg.data);
//for (int q=0; q<3; q++) {
//  MSF[q]=cdm_msg.data[q];
//  }
Mode=cdm_msg.data[0];
Speed=cdm_msg.data[1];
Freq=cdm_msg.data[2];
//Serial.println(Speed);
//Serial.println("HELLO!!!");
}

void message2Cb(const std_msgs::UInt16MultiArray& speed_msg)
{
speed_msg.data;

//Serial.write(speed_msg.data);
for (int q=0; q<36; q++) {
  RPM[q]=speed_msg.data[q];
  }

}

ros::Subscriber<std_msgs::UInt32MultiArray> sub("fan_setup_MSF", &messageCb);
ros::Subscriber<std_msgs::UInt16MultiArray> sub2("faststuff", &message2Cb);
void setup() {
  nh.initNode();
  nh.subscribe(sub);
  nh.subscribe(sub2);
  Serial.begin(256000);
  pwm1.begin();
  pwm1.setPWMFreq(100);  // 1600 is the max, use lower value to prevent "singing"
 
  pwm2.begin();
  pwm2.setPWMFreq(100);
  
  pwm3.begin();
  pwm3.setPWMFreq(100);
  randomSeed(analogRead(0));
  for (int c = 0; c < Freq; c++) {
    p[c] = random(-3, 3);
  scrambleArray(*FID, count); 
}


for (int a=0; a<36; a++)
{
  randomSeed(analogRead(0));
 r = random(a,35);
 int temp = list[a];
 list[a] = list[r];
 list[r] = temp;
}
//  pinMode(3, OUTPUT);
//  pinMode(5, OUTPUT);
//  pinMode(6, OUTPUT);
//  pinMode(9, OUTPUT);
//  pinMode(10, OUTPUT);
//  pinMode(11, OUTPUT);
//Serial.println(list[1]);

}

void loop() {
//  Serial.println(p[4]);
  // laminar 0
if (Mode == 0){
  for (int LAM=0; LAM<12; LAM++){
    pwm1.setPWM(LAM,0,Speed*40.95);
    pwm2.setPWM(LAM,0,Speed*40.95);
    pwm3.setPWM(LAM,0,Speed*40.95);
  }
}
  // shear 1 top bottom
else if (Mode == 1){
  for (int SH1=0; SH1 < 12; SH1++){
    pwm1.setPWM(SH1,0,Speed*40.95);
  }
  for (int SH2=0; SH2 < 6; SH2++){
    pwm2.setPWM(SH2,0,Speed*40.95);
  }
}
  // shear bottom top
else if (Mode == 1000){
  for (int SHBT=0; SHBT < 12; SHBT++){
    pwm3.setPWM(SHBT,0,Speed*40.95);
  }
  for (int SHBT2=6; SHBT2 < 12; SHBT2++){
    pwm2.setPWM(SHBT2,0,Speed*40.95);
  }
}
//shear left on
else if (Mode ==11){
  for (int SH11=0;SH11<3; SH11++){
    pwm1.setPWM(SH11,0,Speed*40.95);
    pwm1.setPWM(SH11+6,0,Speed*40.95);
    pwm2.setPWM(SH11,0,Speed*40.95);
    pwm2.setPWM(SH11+6,0,Speed*40.95);
    pwm3.setPWM(SH11,0,Speed*40.95);
    pwm3.setPWM(SH11+6,0,Speed*40.95);
  }
}
//shear Right on
else if (Mode ==111){
  for (int SH111=3;SH111<6; SH111++){
    pwm1.setPWM(SH111,0,Speed*40.95);
    pwm1.setPWM(SH111+6,0,Speed*40.95);
    pwm2.setPWM(SH111,0,Speed*40.95);
    pwm2.setPWM(SH111+6,0,Speed*40.95);
    pwm3.setPWM(SH111,0,Speed*40.95);
    pwm3.setPWM(SH111+6,0,Speed*40.95);
  }
}
//Shear top left
else if (Mode == 1111){
  for (int SHTL_0=0;SHTL_0<6; SHTL_0++){
    pwm1.setPWM(SHTL_0,0,Speed*40.95);
  }
  
  for (int SHTL_1=6;SHTL_1<11; SHTL_1++){
    pwm1.setPWM(SHTL_1,0,Speed*40.95);
  }
  for (int SHTL_2=0;SHTL_2<4; SHTL_2++){
    pwm2.setPWM(SHTL_2,0,Speed*40.95);
  }
  for (int SHTL_3=6;SHTL_3<9; SHTL_3++){
    pwm2.setPWM(SHTL_3,0,Speed*40.95);
  }
  for (int SHTL_4=0;SHTL_4<2; SHTL_4++){
    pwm3.setPWM(SHTL_4,0,Speed*40.95);
  }
  for (int SHTL_5=6;SHTL_5<7; SHTL_5++){
    pwm3.setPWM(SHTL_5,0,Speed*40.95);
//    pwm1.setPWM(SHTL_0+5,0,0*40.95);
  }
}

//Shear top Right
else if (Mode == 11111){
  for (int SHTR_0=0;SHTR_0<6; SHTR_0++){
    pwm1.setPWM(SHTR_0,0,Speed*40.95);
  }
  for (int SHTR_1=7;SHTR_1<12; SHTR_1++){
    pwm1.setPWM(SHTR_1,0,Speed*40.95);
  }
  for (int SHTR_2=2;SHTR_2<6; SHTR_2++){
    pwm2.setPWM(SHTR_2,0,Speed*40.95);
  }
  for (int SHTR_3=9;SHTR_3<12; SHTR_3++){
    pwm2.setPWM(SHTR_3,0,Speed*40.95);
  }
  for (int SHTR_4=4;SHTR_4<6; SHTR_4++){
    pwm3.setPWM(SHTR_4,0,Speed*40.95);
  }
  for (int SHTR_5=11;SHTR_5<12; SHTR_5++){
    pwm3.setPWM(SHTR_5,0,Speed*40.95);
  }
}
//Shear bottom left
else if (Mode == 10){
  for (int SHBL_0=0;SHBL_0<1; SHBL_0++){
    pwm1.setPWM(SHBL_0,0,Speed*40.95);
  }
  for (int SHBL_1=6;SHBL_1<8; SHBL_1++){
    pwm1.setPWM(SHBL_1,0,Speed*40.95);
  }
  for (int SHBL_2=0;SHBL_2<3; SHBL_2++){
    pwm2.setPWM(SHBL_2,0,Speed*40.95);
  }
  for (int SHBL_3=6;SHBL_3<10; SHBL_3++){
    pwm2.setPWM(SHBL_3,0,Speed*40.95);
  }
  for (int SHBL_4=0;SHBL_4<5; SHBL_4++){
    pwm3.setPWM(SHBL_4,0,Speed*40.95);
  }
  for (int SHBL_5=6;SHBL_5<12; SHBL_5++){
    pwm3.setPWM(SHBL_5,0,Speed*40.95);
  }
}

//Shear Bottom Right
else if (Mode == 100){
  for (int SHBR_0=5;SHBR_0<6; SHBR_0++){
    pwm1.setPWM(SHBR_0,0,Speed*40.95);
  }
  for (int SHBR_1=10;SHBR_1<12; SHBR_1++){
    pwm1.setPWM(SHBR_1,0,Speed*40.95);
  }
  for (int SHBR_2=3;SHBR_2<6; SHBR_2++){
    pwm2.setPWM(SHBR_2,0,Speed*40.95);
  }
  for (int SHBR_3=8;SHBR_3<12; SHBR_3++){
    pwm2.setPWM(SHBR_3,0,Speed*40.95);
  }
  for (int SHBR_4=1;SHBR_4<6; SHBR_4++){
    pwm3.setPWM(SHBR_4,0,Speed*40.95);
  }
  for (int SHBR_5=6;SHBR_5<12; SHBR_5++){
    pwm3.setPWM(SHBR_5,0,Speed*40.95);
  }
}
  // check 2  
else if (Mode == 2){
  for (int CH=0; CH<6; CH+=2){
    pwm1.setPWM(CH,0,Speed*40.95);
    pwm2.setPWM(CH,0,Speed*40.95);
    pwm3.setPWM(CH,0,Speed*40.95);
}

  for (int CH2=7; CH2<12; CH2+=2){
    pwm1.setPWM(CH2,0,Speed*40.95);
    pwm2.setPWM(CH2,0,Speed*40.95);
    pwm3.setPWM(CH2,0,Speed*40.95);
}
}
  // turb 3
else if (Mode == 3){



  for (int CH=0; CH<12; CH++){
    pwm1.setPWM(CH,0,20*40.95);
    pwm2.setPWM(CH,0,20*40.95);
    pwm3.setPWM(CH,0,20*40.95);
}
//  for (int CH1=0; CH1<6; CH1++){
//    pwm3.setPWM(CH1,0,20*40.95);
//}    
delay(2500);
//delay(4000);
//delay(6000);

  for (int CH2=0; CH2<12; CH2++){
    pwm1.setPWM(CH2,0,Speed*40.95);
    pwm2.setPWM(CH2,0,Speed*40.95);
    pwm3.setPWM(CH2,0,Speed*40.95);
}
//  for (int CH3=0; CH3<6; CH3++){
//    pwm3.setPWM(CH3,0,Speed*40.95);
//} 
delay(2500);
//delay(4000);
//delay(6000);
//  Serial.println(Si[1]);
}

  // D-check 4  
else if (Mode == 4){
  t = millis() / 1000.0;
  F = 5.0;
  for (int CH=0; CH<6; CH+=2){
    pwm1.setPWM(CH,0,(40*sin(2*PI/F*t)+60)*40.95);
    pwm2.setPWM(CH,0,(40*sin(2*PI/F*t)+60)*40.95);
    pwm3.setPWM(CH,0,(40*sin(2*PI/F*t)+60)*40.95);
}

  for (int CH3=1; CH3<7; CH3+=2){
    pwm1.setPWM(CH3,0,(40*sin(2*PI/F*t+PI)+60)*40.95);
    pwm2.setPWM(CH3,0,(40*sin(2*PI/F*t+PI)+60)*40.95);
    pwm3.setPWM(CH3,0,(40*sin(2*PI/F*t+PI)+60)*40.95);
}

  for (int CH2=7; CH2<12; CH2+=2){
    pwm1.setPWM(CH2,0,(40*sin(2*PI/F*t)+60)*40.95);
    pwm2.setPWM(CH2,0,(40*sin(2*PI/F*t)+60)*40.95);
    pwm3.setPWM(CH2,0,(40*sin(2*PI/F*t)+60)*40.95);
}
  for (int CH4=6; CH4<11; CH4+=2){
    pwm1.setPWM(CH4,0,(40*sin(2*PI/F*t+PI)+60)*40.95);
    pwm2.setPWM(CH4,0,(40*sin(2*PI/F*t+PI)+60)*40.95);
    pwm3.setPWM(CH4,0,(40*sin(2*PI/F*t+PI)+60)*40.95);
}
}

  // DD-check 5  
else if (Mode == 5){
  t = millis() / 1000.0;
  F = 15.0;
  FF=20.0;
  FFF=25.0;
  for (int CH=0; CH<6; CH+=2){
    pwm1.setPWM(CH,0,(12*sin(2*PI/F*t)+12*sin(2*PI/FF*t)+12*sin(2*PI/FFF*t)+60)*40.95);
    pwm2.setPWM(CH,0,(12*sin(2*PI/F*t)+12*sin(2*PI/FF*t)+12*sin(2*PI/FFF*t)+60)*40.95);
    pwm3.setPWM(CH,0,(12*sin(2*PI/F*t)+12*sin(2*PI/FF*t)+12*sin(2*PI/FFF*t)+60)*40.95);
}

  for (int CH3=1; CH3<7; CH3+=2){
    pwm1.setPWM(CH3,0,(12*sin(2*PI/F*t+PI)+12*sin(2*PI/FF*t+PI)+12*sin(2*PI/FFF*t+PI)+60)*40.95);
    pwm2.setPWM(CH3,0,(12*sin(2*PI/F*t+PI)+12*sin(2*PI/FF*t+PI)+12*sin(2*PI/FFF*t+PI)+60)*40.95);
    pwm3.setPWM(CH3,0,(12*sin(2*PI/F*t+PI)+12*sin(2*PI/FF*t+PI)+12*sin(2*PI/FFF*t+PI)+60)*40.95);
}

  for (int CH2=7; CH2<12; CH2+=2){
    pwm1.setPWM(CH2,0,(12*sin(2*PI/F*t)+12*sin(2*PI/FF*t)+12*sin(2*PI/FFF*t)+60)*40.95);
    pwm2.setPWM(CH2,0,(12*sin(2*PI/F*t)+12*sin(2*PI/FF*t)+12*sin(2*PI/FFF*t)+60)*40.95);
    pwm3.setPWM(CH2,0,(12*sin(2*PI/F*t)+12*sin(2*PI/FF*t)+12*sin(2*PI/FFF*t)+60)*40.95);
}
  for (int CH4=6; CH4<11; CH4+=2){
    pwm1.setPWM(CH4,0,(12*sin(2*PI/F*t+PI)+12*sin(2*PI/FF*t+PI)+12*sin(2*PI/FFF*t+PI)+60)*40.95);
    pwm2.setPWM(CH4,0,(12*sin(2*PI/F*t+PI)+12*sin(2*PI/FF*t+PI)+12*sin(2*PI/FFF*t+PI)+60)*40.95);
    pwm3.setPWM(CH4,0,(12*sin(2*PI/F*t+PI)+12*sin(2*PI/FF*t+PI)+12*sin(2*PI/FFF*t+PI)+60)*40.95);
}
}


//else if (Mode == 6){
//  scrambleArray(numbers, count);
//  Serial.println(numbers[0]);
//  for (int sc = 0; sc <36; sc++) {
//    if (numbers[sc] <= 11) {pwm1.setPWM(numbers[sc],0,Speed*40.95);}
//    else if ((numbers[sc] >= 12) && (numbers[sc] <= 23)) {pwm2.setPWM(numbers[sc]-12,0,Speed*40.95);}
//    else if (numbers[sc] >= 24) {pwm3.setPWM(numbers[sc]-24,0,Speed*40.95);}
//    for (int sc2 = 0; sc2 <36; sc2++) {
//      if ((RPM[sc2]>=1900) && (numbers[sc2] <= 11)) {pwm1.setPWM(numbers[sc2],0,0*40.95);}
//      else if ((RPM[sc2]>=1900) && (numbers[sc2] >= 12) && (numbers[sc2] <= 23)) {pwm2.setPWM(numbers[sc2]-12,0,0*40.95);}
//      else if ((RPM[sc2]>=1900) && (numbers[sc2] >= 24)) {pwm3.setPWM(numbers[sc2]-24,0,0*40.95);}
//    }
//    delay(1000);
//  }
//  
//}

//else if (Mode == 6){
//
//  for (int i =0; i< 36; i++) {
//    if ((FID [i][1] == 0) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,Speed*40.95);FID [i][1]=1;}
//    else if ((FID[i][1] == 0) && (FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,Speed*40.95);FID [i][1]=1;}
//    else if ((FID[i][1] == 0) && (FID[i][0] >=24)) {pwm3.setPWM(FID[i][0]-24,0,Speed*40.95);FID [i][1]=1;}
//    if ((FID[i][1] == 1) && (FID[i][0] <=11) && (RPM[FID[i][0]] >=1900)) {pwm1.setPWM(FID[i][0],0,0*40.95);FID [i][1]=0;}
//    else if ((FID[i][1] == 1) && (FID[i][0] >=12) && (FID[i][0] <=23) && (RPM[FID[i][0]] >=1900)) {pwm2.setPWM(FID[i][0]-12,0,0*40.95);FID [i][1]=0;}
//    else if ((FID[i][1] == 1) && (FID[i][0] >=24) && (RPM[FID[i][0]] >=1900)) {pwm3.setPWM(FID[i][0]-24,0,0*40.95);FID [i][1]=0;}
//    
//  }
//  
// }

else if (Mode == 6){
  for (int i =0; i< 36; i++) {
    toss[i]=random(0,2);
  
//    if ((toss[i] == 0) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,Speed*40.95);}
//    else if ((toss[i] == 0) && (FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,Speed*40.95);}
//    else if ((toss[i] == 0) && (FID[i][0] >=24)) {pwm3.setPWM(FID[i][0]-24,0,Speed*40.95);}
//    else if ((toss[i] == 1) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,20*40.95);}
//    else if ((toss[i] == 1) &&(FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,20*40.95);}
//    else if ((toss[i] == 1) &&FID[i][0] >=24) {pwm3.setPWM(FID[i][0]-24,0,20*40.95);}

    if ((toss[i] == 0) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,Speed*40.95);}
    else if ((toss[i] == 0) && (FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,Speed*40.95);}
    else if ((toss[i] == 0) && (FID[i][0] >=24)) {pwm3.setPWM(FID[i][0]-24,0,Speed*40.95);}
    else if ((toss[i] == 1) && (FID[i][0] <=11)) {pwm1.setPWM(FID[i][0],0,0*40.95);}
    else if ((toss[i] == 1) &&(FID[i][0] >=12) && (FID[i][0] <=23)) {pwm2.setPWM(FID[i][0]-12,0,0*40.95);}
    else if ((toss[i] == 1) &&FID[i][0] >=24) {pwm3.setPWM(FID[i][0]-24,0,0*40.95);}
  }
  delay(1000);
}



 nh.spinOnce(); 
}


float gen_sig(float x[10], float y) {
  float s[10];
  for (int j = 1; j < 10 + 1; j++) {
    s[j - 1] = sin((j /10.0* 2 * PI * y) + x[j - 1]) * 10;
//    Serial.println(x[2]);


  }
  
  int ss = 0;
  for (int i = 0; i < 10; i++) {
    ss += s[i];
    if (i == 10-1) ss = ss + Speed;

//        Serial.println(ss);
  }
//  Serial.println(MSF[1]);
  if (ss >= 100) ss = 100;
  if (ss <= 20) ss = 20;
//  Serial.println(ss);
  return ss;
}

float gen_time (float y, int n) {
  float TIME;
  TIME = y + 100 * (n);
  return TIME;
}

float gen_phase() {
  //  for (int i = 0; i < 10; i++) {

  float P;
  P = random(-PI, PI);
  return P;
}

void scrambleArray(int * array, int size)
{
  int last = 0;
  int temp = array[last];
  for (int i=0; i<size; i++)
  {
    int index = random(size);
    array[last] = array[index];
    last = index;
  }
  array[last] = temp;
}
