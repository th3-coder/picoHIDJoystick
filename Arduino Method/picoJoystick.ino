int x, y;

void setup() {
  // put your setup code here, to run once:
  pinMode(26, INPUT);
  pinMode(27, INPUT);
  Serial.begin(115200);
}

void loop() {
  //determine x value
  x = analogRead(26) - 505;

  /* test output
  Serial.print("x: "); 
  Serial.print(x);
  Serial.print("\n");
  */

  if (x > 24)
    x = 0; //right
  else if (x < -24)
    x = 2; //left
  else
    x = 1; //center

  //determine y value
  y = analogRead(27) - 510;

  /* test output
    Serial.print("y: "); 
  Serial.print(y);
  Serial.print("\n");
  */

  if (y > 24)
    y = 0; //down
  else if (y < -24)
    y = 2; //up
  else
    y = 1; //center
  
  Serial.print("S");  //start printing the data, format is Sxc,yc,buttonStates > S1,1,0
  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print("\n");

  delay(10);
}