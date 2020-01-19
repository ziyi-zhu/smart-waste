#include <Servo.h>

const int trigPin = 9;
const int echoPin = 10;
const int ledPin = 13;
const int buttonPin = A0;

// defines variables
long duration;
int distance;
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 90;    // variable to store the servo position
int isFull = false;
int thres = 15;
int timer = 0;

int getDistance() {
  // Ultrasonic censor set up
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculating the distance
  return duration*0.034/2;
}

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);

  Serial.begin(9600); // Starts the serial communication
  myservo.attach(11);  // attaches the servo on pin 9 to the servo object

  digitalWrite(ledPin, LOW);
}

void loop() {
  distance = getDistance();
  
  // Find out full or not
  if(distance < thres && !isFull){
    delay(3000);
    
    distance = getDistance();
    if(distance < thres) {
      digitalWrite(ledPin, HIGH);
      isFull = true;
    }                 
  }
  else if(distance > thres && isFull){
    delay(3000);
    
    distance = getDistance();
    if(distance > thres) {
      digitalWrite(ledPin, LOW);
      isFull = false;
    }                 
  }
  
  if(digitalRead(buttonPin) == HIGH) {
    Serial.println('x');

    while(Serial.available() == 0) {
      continue;
    }

    char x = Serial.read();

    if(x == 'u') {
      for (int deg = pos; deg <= 135; deg++) {
        myservo.write(deg);
        pos = deg;
        delay(10);
      } 
      for (int deg = pos; deg >= 90; deg--) {
        myservo.write(deg);
        pos = deg;
        delay(10);
      }
    }
    else if(x == 'd') {
      for (int deg = pos; deg >= 45; deg--) {
        myservo.write(deg);
        pos = deg;
        delay(10);
      } 
      for (int deg = pos; deg <= 90; deg++) {
        myservo.write(deg);
        pos = deg;
        delay(10); 
      }
    }
  }
  
  if(Serial.available() > 0) {
    char instruction = Serial.read();

    if(instruction == '0') {
      for (int deg = pos; deg >= 0; deg--) {
        myservo.write(deg);
        pos = deg;
        delay(10);
      }        
    }
    else if(instruction == '1') {
      for (int deg = pos; deg <= 90; deg++) {
        myservo.write(deg);
        pos = deg;
        delay(10);
      } 
    }
    else if(instruction == '2') {
      for (int deg = pos; deg <= 180; deg++) {
        myservo.write(deg);
        pos = deg;
        delay(10);
      } 
    }
  }                
}
