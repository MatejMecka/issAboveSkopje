const int aPinLed = 12;
const int bPinLed = 10;
const int cPinLed = 11;
const int dPinLed = 13;
char mydata=0;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(aPinLed, OUTPUT);
  pinMode(bPinLed, OUTPUT);
  pinMode(cPinLed, OUTPUT);
  pinMode(dPinLed, OUTPUT);
    
    Serial.begin(9600);
}


// the loop routine runs over and over again forever:
void loop() {
  
 mydata= int(Serial.read());


if (mydata=='1') {
  for (int i = 0; i < 20; i++) {
    digitalWrite(aPinLed, HIGH);
    delay(100);
    digitalWrite(aPinLed, LOW);
    delay(100);
  
    digitalWrite(cPinLed, HIGH);
    delay(100);
    digitalWrite(cPinLed, LOW);
    delay(100);
  
    digitalWrite(bPinLed, HIGH);
    delay(100);
    digitalWrite(bPinLed, LOW);
    delay(100);
  
    digitalWrite(dPinLed, HIGH);
    delay(100);
    digitalWrite(dPinLed, LOW);
    delay(100);
}
}
if(mydata=='0'){
  digitalWrite(aPinLed, LOW);
  
  digitalWrite(bPinLed, LOW);

  digitalWrite(cPinLed, LOW);

  digitalWrite(dPinLed, LOW);  
}
}
  


