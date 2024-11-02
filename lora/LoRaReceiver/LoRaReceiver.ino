//code adapted from https://github.com/HelTecAutomation/CubeCell-Arduino/tree/master/libraries/LoRa/examples/LoRaBasic
#include "LoRaWan_APP.h"
#include "Arduino.h"
/*
 * set LoraWan_RGB to 1,the RGB active in loraWan
 * RGB red means sending;
 * RGB green means received done;
 */
#ifndef LoraWan_RGB
#define LoraWan_RGB 0
#endif

#define RF_FREQUENCY                                915000000 // Hz

#define TX_OUTPUT_POWER                             14        // dBm

#define LORA_BANDWIDTH                              0         // [0: 125 kHz,
                                                              //  1: 250 kHz,
                                                              //  2: 500 kHz,
                                                              //  3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5,
                                                              //  2: 4/6,
                                                              //  3: 4/7,
                                                              //  4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false


#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 30 // Define the payload size here

double MAX_TURN = 45; //below abs value = turning is ok (yaw)
                    //e.g. if MAX_TURN is 45, any angle between -45 to 45, and 135 to 225 is ok to turn (yaw).

char txpacket[BUFFER_SIZE];
char rxpacket[BUFFER_SIZE];

static RadioEvents_t RadioEvents;

int16_t txNumber;

int16_t rssi,rxSize;
bool lora_idle = true;

void setup() {
    Serial.begin(115200);

    txNumber=0;
    rssi=0;
  
    RadioEvents.RxDone = OnRxDone;
    Radio.Init( &RadioEvents );
    Radio.SetChannel( RF_FREQUENCY );
  
    Radio.SetRxConfig( MODEM_LORA, LORA_BANDWIDTH, LORA_SPREADING_FACTOR,
                                   LORA_CODINGRATE, 0, LORA_PREAMBLE_LENGTH,
                                   LORA_SYMBOL_TIMEOUT, LORA_FIX_LENGTH_PAYLOAD_ON,
                                   0, true, 0, 0, LORA_IQ_INVERSION_ON, true );

   }



void loop()
{
  if(lora_idle)
  {
  	turnOffRGB();
    lora_idle = false;
    Serial.println("into RX mode");
    Radio.Rx(0);

  }
  //Serial.println(rxpacket);
  String cmds = rxpacket;
  cmds = cmds.substring(1, cmds.length()-1);
  int values[7];

  int i = 0;
  while(i < 7){
     int ind = cmds.indexOf(",");
     values[i] = cmds.substring(0,ind).toInt();
     cmds = cmds.substring(ind+1);
     i++;
  }

  int forward = values[3];
  int down = values[0];
  int up = values[1];
  up = up-down;

  up = -up;
  double f = forward;

  double angle = 0.0;
  if(f == 0){
    if(up > 0){
      angle = 90;
    }
    else{
      angle = 270;
    }
  }
  else{
    
    angle = atan(up/f)*(180/3.14159);
  
    if(f > 0){angle += 180;}
  }

  //thrust = -movement
  angle = (angle + 180);
  angle = angle+360.0;

  //angle = angle % 360.0;
  // ^^ WHY DOESNT THAT EXIST

   
  while(angle > 360.0){angle -= 360.0;}
  
  Serial.print(angle);
  double dist2X = 0.0;
  if(angle > 90 && angle < 270){
    dist2X = abs(180-angle);
  }
  if(angle < 90){
    dist2X = angle;
  }
  if(angle > 270){
    dist2X = 360-angle;
  }
  if(angle == 90 or angle == 270){
    dist2X = 90;
  }
  Serial.print(" ");
  Serial.print(dist2X);
  Serial.print(" ");

  double turnability = 0.0;
  if(dist2X <= MAX_TURN){
    double x = dist2X /MAX_TURN;
     turnability = 1-x;
  }

   //no turnings = yaw def ok
 /* may not need */
  if(values[3] == 0 and values[0]==0 and values[1]==0){
    turnability = 1;
  }
  
  Serial.print(turnability);
  Serial.print(" ");


  
  double turnings = values[4];
  turnings = turnings * 100.0/9.0;

  turnings *= turnability;
  Serial.print(turnings);
  double leftspeed = 100;
  double rightspeed = 100;
  if(turnings < 0){
    leftspeed += turnings;
  }
  else{
    rightspeed -= turnings;
  }
  //determine the magnitude.
  float mag = sqrt(up*up + forward*forward);
  if(mag > 9){mag = 9;}
  mag = mag/9.0;
  
  Serial.print("\t\t\t");
  Serial.print("D: ");
  Serial.print(angle);
  Serial.print("  M: ");
  Serial.print(mag);

  leftspeed *= mag;
  rightspeed *= mag;
  
  Serial.print("  L: ");
  Serial.print(leftspeed);
  Serial.print("  R: ");
  Serial.print(rightspeed);

  
  Serial.println();

  
}

void OnRxDone( uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr )
{
    rssi=rssi;
    rxSize=size;
    memcpy(rxpacket, payload, size );
    rxpacket[size]='\0';
    turnOnRGB(COLOR_RECEIVED,0);
    Radio.Sleep( );
    Serial.printf("\r\nreceived packet \"%s\" with rssi %d , length %d\r\n",rxpacket,rssi,rxSize);
    lora_idle = true;
}
