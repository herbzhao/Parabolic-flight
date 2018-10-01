// PID_AutoTune_v0 - Version: Latest 
#include <PID_v1.h>
#include <PID_AutoTune_v0.h>
double PID_setpoint, PID_input, PID_output;
//Define the aggressive and conservative Tuning Parameters
// https://robotics.stackexchange.com/questions/9786/how-do-the-pid-parameters-kp-ki-and-kd-affect-the-heading-of-a-differential
double Kp=1000, Ki=50, Kd=50;
//Specify the links and initial tuning parameters
PID myPID(&PID_input, &PID_output, &PID_setpoint, Kp, Ki, Kd, REVERSE);

// peltier
#define peltier_pin 9    // LED connected to digital pin 9

// LEDs
#include <Adafruit_NeoPixel.h>
#define Neopixel_PIN 6
#define num_LEDs 12
Adafruit_NeoPixel LEDs = Adafruit_NeoPixel(num_LEDs, Neopixel_PIN, NEO_GRB + NEO_KHZ800);
// starting LED colour
int r=0, g=0, b=0;

// Thermistor
// which analog pin to connect
#define thermistor_pin A0         
// temp. for nominal resistance (almost always 25 C)
#define temperature_norminal 25   
// resistance at 25 degrees C
#define thermistor_norminal_resistance 100000   
// The beta coefficient of the thermistor (usually 3000-4000)
#define B_coefficient 3950
// the value of the serial resistor
#define reference_resistor 100000    
// how many analogue_readings to take and average, more takes longer
// but is more 'smooth'
#define number_of_analogue_measurements 10
// set some variables for thermistor
uint16_t analogue_readings[number_of_analogue_measurements];
uint8_t i;
float average_analogue_reading;


// global varialbes for the code
String serial_input;
float temperature;
// gap between each measurment and adjustment in seconds
#define delay_time 0.2

// Average the temperature measurement to ensure a stable temperature control
#define number_of_temp_measurements 20
int j = 1;
float temperatures[number_of_temp_measurements];
float average_temperature;

// final goal of temperature
#define PID_starting_setpoint 19
#define PID_final_setpoint 10
// this is the step that PID setpoint change each time 
// (smaller = longer = less overshoot)
#define PID_setpoint_change_step 0.2
// this is temperature fluctuation range that is acceptable before changing PID_setpoint
// (smaller = longer time to reach stability = less chance of false positive )
#define PID_fluctuation_range 0.05


void setup(void) {
  // start serial port
  Serial.begin(9600);
  Serial.setTimeout(50);
  
  //initialize the variables we're linked to
  PID_setpoint = PID_starting_setpoint;
  myPID.SetOutputLimits(0, 255);

  //turn the PID on
  myPID.SetMode(AUTOMATIC);
  
  //start the LED
  LEDs.begin();
  LED_colour(r,g,b);
}


void loop(void) {
  PID_input = read_temperature();
  temperatures[j] =  PID_input;
  
  // check if the average temperature is stable within range
  // then adjust PID_setpoint with small step to prevent overshoot
  measure_average_temp_and_adjust_PID_setpoint();

// TODO: a way to control cooling rate? C/min

  // PID control the peltier cooling effort
  myPID.Compute();
  analogWrite(peltier_pin, PID_output);

  // To read serial input
  if (Serial.available()) 
  {
    serial_input = Serial.readString();
    serial_condition(serial_input);  
  }

  // wait for next temperature measurement
  delay(delay_time*1000);
}


float read_temperature(){
  // take N analogue_readings in a row, with a slight delay
  for (i=0; i< number_of_analogue_measurements; i++) {
    analogue_readings[i] = analogRead(thermistor_pin);
    delay(10);
  }
 
  // average all the analogue_readings out
  average_analogue_reading = 0;
  for (i=0; i< number_of_analogue_measurements; i++){
    average_analogue_reading += analogue_readings[i];
  }
  average_analogue_reading /= number_of_analogue_measurements;
  
  // convert the voltage value to resistance
  average_analogue_reading = 1023 / average_analogue_reading - 1;
  average_analogue_reading = reference_resistor / average_analogue_reading;
  temperature = average_analogue_reading / thermistor_norminal_resistance;     // (R/Ro)
  temperature = log(temperature);                  // ln(R/Ro)
  temperature /= B_coefficient;                   // 1/B * ln(R/Ro)
  temperature += 1.0 / (temperature_norminal + 273.15); // + (1/To)
  temperature = 1.0 / temperature;                 // Invert
  temperature -= 273.15;                         // convert to C
  
  // also get a time variable
  float time;
  time = float(millis())/float(1000);
  Serial.print(time);    //prints time since program started
  Serial.println(" s");

  // temeperature  
  Serial.print(temperature);
  Serial.println(" *C");
  
  // return value
  return temperature;
}


// move the temperature down slowly to ensure a smooth curve?
void adjust_PID_setpoint() {
  // when temperature stablise then reduce setpoint again
  if (abs(average_temperature-PID_setpoint)< PID_fluctuation_range){
    // only move the setpoint if it is not the final_setpoint
    // When comparing float, tiny difference that generates somewhere will cause problem
    // convert float into int and then compare
    if (int(PID_setpoint*100) != int(PID_final_setpoint*100)){
      // decrease the setpoint by tiny bit each time
      PID_setpoint -= PID_setpoint_change_step;
    }
    else{
      //Serial.println("Reached the designated temperature");
    }
  }
}


void measure_average_temp_and_adjust_PID_setpoint(){
    // measure the average temperature
  if (j < number_of_temp_measurements){ 
    j +=1;
  }
  else{
    for (j=1; j<=number_of_temp_measurements; j++){
      average_temperature += temperatures[j];
    }
    average_temperature = float(average_temperature)/float(number_of_temp_measurements);
    // check whether to change PID values if the temperature is stable
    adjust_PID_setpoint();
    // reset everything
    j = 1;
    average_temperature = 0;
  }
}


void serial_condition(String serial_input){
  //Serial.println(serial_input);
  // trim is needed as there is blank space and line break
  serial_input.trim();
  if (serial_input == "66" or serial_input == "led_on"){
    LED_colour(255,255,255);
  }
  else if (serial_input == "-66" or serial_input == "led_off"){
    LED_colour(0,0,0);
  }
}


void LED_colour(int r, int g, int b) {
  for (int i = 0; i < num_LEDs; i++) {
    // LED.Color takes RGB values, from 0,0,0 up to 255,255,255
    LEDs.setPixelColor(i, LEDs.Color(r, g, b)); // Moderately bright green color.
    LEDs.show(); // This sends the updated pixel color to the hardware.
    delay(5);
  }
}