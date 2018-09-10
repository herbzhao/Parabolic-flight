// which analog pin to connect
#define THERMISTORPIN A0         
// resistance at 25 degrees C
#define THERMISTORNOMINAL 100000   
// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 3950
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25   
// the value of the serial resistor
#define SERIESRESISTOR 100000    
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5



// set some variables
uint16_t samples[NUMSAMPLES];
uint8_t i;
float average;
int peltier_signal = 9;    // LED connected to digital pin 9
float temperature;
float gradient;
float cooling_effort;
int delay_time;

void setup(void) {
  // start serial port
  Serial.begin(9600);
  Serial.setTimeout(50);
  // a random number to initialise the program
  temperature = 30;
  // initial cooling effort
  cooling_effort = 0.2;
  // gap between each measurment and adjustment in seconds
  delay_time = 2;
}
 
void read_temperature()
{
  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(THERMISTORPIN);
   delay(10);
  }
 
  // average all the samples out
  average = 0;
  for (i=0; i< NUMSAMPLES; i++) {
     average += samples[i];
  }
  average /= NUMSAMPLES;
  
  //Serial.print("Average analog reading "); 
  //Serial.println(average);
 
  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
  //Serial.print("Thermistor resistance "); 
  //Serial.println(average);
 
  float temperature_0;
  float temperature_1;
  // previous temperature 
  temperature_0 = temperature;

  temperature = average / THERMISTORNOMINAL;     // (R/Ro)
  temperature = log(temperature);                  // ln(R/Ro)
  temperature /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  temperature += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  temperature = 1.0 / temperature;                 // Invert
  temperature -= 273.15;                         // convert to C

  // new temperature
  temperature_1 = temperature;
  
  // also get a time variable
  unsigned long time;
  time = millis()/1000;
  Serial.print(time);    //prints time since program started
  Serial.println(" s");

  // temeperature  
  Serial.print(temperature);
  Serial.println(" *C");

  // temperature gradient per min
  gradient = (temperature_1-temperature_0)/delay_time*60;
}


float peltier_cooling(float cooling_effort)
{
  analogWrite(peltier_signal, cooling_effort*255);
}

float cooling_effort_controller()
{
  // if cooling faster than 2 C/min, reduce cooling effort
  if (gradient < -2)
  {
    cooling_effort = cooling_effort - 0.02;
  }
  // if within 2 degree, stay unchanged
  else if (gradient > -2 && gradient <-0.5)
  {
    cooling_effort = cooling_effort;
  }
  else
  {
    cooling_effort = cooling_effort + 0.02;
  }
}
 

void loop(void) {
  read_temperature();
  peltier_cooling(cooling_effort);
  cooling_effort_controller();
  Serial.print("cooling effort is: ");
  Serial.println(cooling_effort);
  Serial.print("gradient is:");
  Serial.println(gradient);
  delay(delay_time*1000);
}
