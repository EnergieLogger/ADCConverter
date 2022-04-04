import sched, time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Timer
import json

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
meetwaarden = [0]*500;


def spanning_meten():

 for x in range(100): #array vullen met meetwaarden dmv for loop
  print(chan.value)
    
  meetwaarden.insert(x, chan.value); #omrekening van analoge waarde naar spanning (dus *3.3V)
    
  maxWaarde = meetwaarden[0]; #de init waarde van max is de eerste plek in de array
   
 for x in range(100):#De for loop doorloopt de volledige array
    
    if(maxWaarde < meetwaarden[x]): #als de volgende array kleiner is dan max was dan krijgt max een nieuwe waarde.
        
        maxWaarde = meetwaarden[x];
 Timer(1, spanning_meten).start() #iedere seconde wordt de functie voor het meten van de spanning aangeroepen




            
        
    
 topwaarde_werkelijk = maxWaarde *144.4; #de werkelijke waarde van de spanning is de max spanning keer een versterkingsfactor
 effectiefgemeten_spanning = topwaarde_werkelijk*0.707; #om van topwaarde naar effectief te gaan wordt vermenigvuldigt met 0,5wortel2 (0,7071)
 data = {

     'Topwaarde spanning': maxWaarde,
     'Topwaarde werkelijk': topwaarde_werkelijk,
     'Effectief gemeten spanning': effectiefgemeten_spanning 
 }

 json_string = json.dumps(data)
 print(json_string)
 print("Topwaarde spanning = %1.3fV  Topwaarde werkelijk = %1.3fV    Effectief gemeten spanning = %1.3fV\n", max, topwaarde_werkelijk, effectiefgemeten_spanning);

spanning_meten()
 