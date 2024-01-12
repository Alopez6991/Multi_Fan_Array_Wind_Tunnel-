#include <ros.h>
#include <std_msgs/UInt16MultiArray.h>
ros::NodeHandle nh;
std_msgs::UInt16MultiArray arr;
ros::Publisher pub_arr( "faststuff", &arr);

//unsigned int timeP[]={t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,t32,t33,t34,t35};
int timeP[36];
int rpm[36];
int OP[]={17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53};
//int OP[]=linspace(17,53);
void setup() {
 nh.initNode();
//  for(int a = 0; a < sizeof(OP)/sizeof(int); a++){
//     pinMode(OP[a], OUTPUT); 
//    }
  Serial.begin(115200);
   for(int a = 0; a < sizeof(OP)/sizeof(int); a++){
     digitalWrite(OP[a], HIGH); 
    } 

 arr.data = (std_msgs::UInt16MultiArray::_data_type*) malloc(2 * sizeof(std_msgs::UInt16MultiArray::_data_type));
 arr.data_length = 36;
 nh.advertise(pub_arr);
// nh.advertise(sendData1);
}
void loop() {
   for(int a = 0; a < sizeof(OP)/sizeof(int); a++){
    timeP[a] = pulseIn(OP[a],HIGH,100000);
//    if (round(timeP[a] == 0)) timeP[a]= (1000000*60)/4;
    rpm [a]=round((1000000*60)/(timeP[a]*4.0));
//    if (round(rpm[a])>65534); rpm[a] = 0;
    arr.data[a]=rpm[a];
    }
 
 pub_arr.publish(&arr);
 nh.spinOnce();
}
