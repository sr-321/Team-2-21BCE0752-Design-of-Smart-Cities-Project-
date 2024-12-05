#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

const int trigPin = 9;        
const int echoPin = 10;       
const int buzzerPin = 4;      
const int safeDistance = 200;  


Servo servo1, servo2, servo3, servo4; 
const int servoPins[] = {5, 6, 7, 8}; 
int servoAngles[] = {0, 0, 0, 0};     

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();


  servo1.attach(servoPins[0]);
  servo2.attach(servoPins[1]);
  servo3.attach(servoPins[2]);
  servo4.attach(servoPins[3]);


  for (int i = 0; i < 4; i++) {
    servoAngles[i] = 0;
    writeServoAngle(i, servoAngles[i]);
  }

  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);

  int distance = duration * 0.034 / 2;

  lcd.setCursor(0, 0);
  lcd.print("Distance: ");
  lcd.print(distance);
  lcd.print(" cm   "); 


  if (distance > 0 && distance < safeDistance) {
    int beepDelay = map(distance, 1, safeDistance, 50, 500);
    int speed = map(distance, 1, safeDistance, 50, 2000); 
    lcd.setCursor(0, 1);
    lcd.print("Alert! Slowing  ");

    tone(buzzerPin, map(distance, 1, safeDistance, 2000, 500)); 
    delay(beepDelay);          
    noTone(buzzerPin);     
    delay(beepDelay); 

    for (int i = 0; i < 4; i++) {
      servoAngles[i] += 5; 
      if (servoAngles[i] > 180) servoAngles[i] = 180;
      writeServoAngle(i, servoAngles[i]);
    }
    delay(speed); 

  }
  else if (distance > 0 && distance < (safeDistance+50)){
    lcd.setCursor(0, 1);
    lcd.print("Alert!          ");
  } 
  else if (distance >= safeDistance || distance <= 0) {
    lcd.setCursor(0, 1);
    lcd.print("All Clear       ");
    noTone(buzzerPin);

    for (int i = 0; i < 4; i++) {
      servoAngles[i] = 0;
      writeServoAngle(i, servoAngles[i]);
    }
    delay(100);
  }
}


void writeServoAngle(int servoIndex, int angle) {
  switch (servoIndex) {
    case 0:
      servo1.write(angle);
      break;
    case 1:
      servo2.write(angle);
      break;
    case 2:
      servo3.write(angle);
      break;
    case 3:
      servo4.write(angle);
      break;
  }
}
