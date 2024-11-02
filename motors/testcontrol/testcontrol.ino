
#define left1 5
#define left2 6

#define right1 9
#define right2 10


void setup(){
  Serial.begin(9600);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void writeLeft(int value){
  if(value < 0){//reverse
    analogWrite(left1, 0);
    analogWrite(left2, -value);
  }
  else{
    analogWrite(left1, value);
    analogWrite(left2, 0);
  }
}

void writeRight(int value){
  if(value < 0){//reverse
    analogWrite(right1, 0);
    analogWrite(right2, -value);
  }
  else{
    analogWrite(right1, value);
    analogWrite(right2, 0);
  }
}

void loop(){
//  if(ain < 0){ //left (forward)
//    analogWrite(left1, -ain*2); //1024
//    analogWrite(left2, 0); //0
//  }
//  else{ //right (reverse)
//    analogWrite(left1, 0); //0
//    analogWrite(left2, ain*2); //1024
//  }
//
//  if(ain < 0){ //left (forward)
//    analogWrite(right1, -ain*2); //1024
//    analogWrite(right2, 0); //0
//  }
//  else{ //right (reverse)
//    analogWrite(right1, 0); //0
//    analogWrite(right2, ain*2); //1024
//  }

  int LJ = analogRead(A0);
  int RJ = analogRead(A1);

  float mult = (LJ-512)/512.0;
  int lval = 1023;
  int rval = 1023;
  
  if(RJ < 511){
    lval += (RJ-511)*4;
  }
  if(RJ > 512){
    rval += (512-RJ)*4;  
  }

  lval *= mult;
  rval *= mult;

  writeLeft(lval);
  writeRight(rval);

  Serial.println(String(lval) + " "+String(rval));



  
  delay(40);
}
