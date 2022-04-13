#include <XInput.h>

bool sync = false;

int xInputPin = 0;
volatile bool setX = false;
int yInputPin = 1;
volatile bool setY = false;
int bInputPin = 2;
volatile bool setB = false;
int aInputPin = 3;
volatile bool setA = false;
int rInputPin = 4;
volatile bool setR = false;
int lInputPin = 5;
volatile bool setL = false;
int startInputPin = 6;
volatile bool setStart = false;
int selectInputPin = 7;
volatile bool setSelect = false;
int rightInputPin = 8;
volatile bool setRight = false;
int leftInputPin = 9;
volatile bool setLeft = false;
int downInputPin = 10;
volatile bool setDown = false;
int upInputPin = 11;
volatile bool setUp = false;

void setPinAndInterrupt(int pin, void * enableMethod) {
  pinMode(pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pin), enableMethod, CHANGE);
}


void setup() {
  // shoulder buttons
  setPinAndInterrupt(rInputPin, RButtonPress);
  setPinAndInterrupt(lInputPin, LButtonPress);
  
  // face buttons
  setPinAndInterrupt(xInputPin, XButtonPress);
  setPinAndInterrupt(yInputPin, YButtonPress);
  setPinAndInterrupt(bInputPin, BButtonPress);
  setPinAndInterrupt(aInputPin, AButtonPress);


  // control buttons
  setPinAndInterrupt(startInputPin, StartButtonPress);
  setPinAndInterrupt(selectInputPin, SelectButtonPress);

  // dpad
  setPinAndInterrupt(rightInputPin, RightButtonPress);
  setPinAndInterrupt(leftInputPin, LeftButtonPress);
  setPinAndInterrupt(downInputPin, DownButtonPress);
  setPinAndInterrupt(upInputPin, UpButtonPress);
  XInput.setAutoSend(false);  // Wait for all controls before sending

  XInput.begin();
}

void XButtonPress(){
  setX = digitalRead(xInputPin);
}
void YButtonPress(){
  setY = digitalRead(yInputPin);
}
void BButtonPress(){
  setB = digitalRead(bInputPin);
}
void AButtonPress(){
  setA = digitalRead(aInputPin);
}
void RButtonPress(){
  setR = digitalRead(rInputPin);
}
void LButtonPress(){
  setL = digitalRead(lInputPin);
}
void StartButtonPress(){
  setStart = digitalRead(startInputPin);
}
void SelectButtonPress(){
  setSelect = digitalRead(selectInputPin);
}
void UpButtonPress(){
  setUp = digitalRead(upInputPin);
}
void RightButtonPress(){
  setRight = digitalRead(rightInputPin);
}
void DownButtonPress(){
  setDown = digitalRead(downInputPin);
}
void LeftButtonPress(){
  setLeft = digitalRead(leftInputPin);
}

void loop() {  
  XInput.setButton(BUTTON_X, setX);
  XInput.setButton(BUTTON_Y, setY);
  XInput.setButton(BUTTON_A, setA);
  XInput.setButton(BUTTON_B, setB);
  XInput.setButton(BUTTON_RB, setR);
  XInput.setButton(BUTTON_LB, setL);
  XInput.setButton(BUTTON_START, setStart);
  XInput.setButton(BUTTON_BACK, setSelect);
  XInput.setDpad(setUp, setDown, setLeft, setRight);
  XInput.send();
  delay(50);
}
