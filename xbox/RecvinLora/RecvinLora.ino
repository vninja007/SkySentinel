void setup(){
   
  // Set the baud rate  
  Serial.begin(115200);
   
}
 
void loop(){
  
 
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.println(data);
  }

}
