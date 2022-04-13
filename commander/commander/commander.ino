int upPin = 1;
int downPin = 2;
int leftPin = 3;
int rightPin = 4;
int selectPin = 5;
int startPin = 6;
int lPin = 7;
int rPin = 8;
int aPin = 9;
int bPin = 10;
int yPin = 11;
int xPin = 12;
int command;

void pressButton(int pin, int duration){
  digitalWrite(pin, HIGH);
  delay(duration);
  digitalWrite(pin, LOW);
}


void setup() {
  pinMode(upPin, OUTPUT);
  pinMode(downPin, OUTPUT);
  pinMode(rightPin, OUTPUT);
  pinMode(leftPin, OUTPUT);
  pinMode(selectPin, OUTPUT);
  pinMode(startPin, OUTPUT);
  pinMode(lPin, OUTPUT);
  pinMode(rPin, OUTPUT);
  pinMode(aPin, OUTPUT);
  pinMode(bPin, OUTPUT);
  pinMode(yPin, OUTPUT);
  pinMode(xPin, OUTPUT);
  Serial.begin(345600);
}

void loop() {
  if (Serial.available()){
    command = Serial.read();
    pressButton(command, 50);
  }
}
