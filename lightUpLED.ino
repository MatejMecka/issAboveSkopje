int led = 13;
char mydata=0;
// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);     
    Serial.begin(9600);
}


// the loop routine runs over and over again forever:
void loop() {
  
 mydata= int(Serial.read());


if (mydata=='1') {
  for (int i = 0; i < 20; i++) {
    digitalWrite(led, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    delay(100);
}
}
if(mydata=='0'){
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
}
}
