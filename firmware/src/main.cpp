#include <Arduino.h>

#define PUL_PIN 2
#define SPK_PIN 3

#define PUL_LONG 6000
#define PUL_SHORT 630
#define PUL_TIMEOUT 6000

#define EMA_K 2

#define SEND_PERIOD_MS 10

volatile unsigned long last_fall;
volatile unsigned long dt, dt_ema;
uint16_t prev_send;
// dt_ema = (dt + (dt_ema << EMA_K)-dt_ema) >> EMA_K;
void on_fall(){
  unsigned long now = micros();
  if(now - last_fall < PUL_LONG){
    dt = now - last_fall;
    last_fall = now;
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(PUL_PIN), on_fall, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long now = micros();
  if(now- last_fall > PUL_TIMEOUT){
    last_fall = now;
    dt = 0;
  }
  Serial.write((uint8_t*)&dt, 2);
}