int sensorPin = A0;
int sensorValue = 0;
float temp = 0.0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(sensorPin);
  float voltage = sensorValue * (5000 / 1024.0);
  temp = (voltage - 500)/10;
  Serial.println(temp);
  delay (500);
}