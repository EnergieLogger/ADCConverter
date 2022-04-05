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
chanstroom = AnalogIn(ads, ADS.P1)
meetwaarden = [0]*100;
meetwaardenstroom = [0]*100;
def stroom_meten():
    
 for x in range(99):
  
  meetwaardenstroom.insert(x, chan.voltage);
  
  maxWaardeStroom = meetwaardenstroom[0]
 for x in range(99):
     if(maxWaardeStroom < meetwaardenstroom[x]):
         
         maxWaardeStroom = meetwaardenstroom[x];
 Timer(1, stroom_meten).start()
 
 topwaarde_werkelijkStroom = (maxWaardeStroom - 1.671)*10;
 print(topwaarde_werkelijkStroom, "A")
    
    
    

def spanning_meten():

 for x in range(99): #array vullen met meetwaarden dmv for loop
    
  meetwaarden.insert(x, chan.voltage); #omrekening van analoge waarde naar spanning (dus *3.3V)
    
  maxWaarde = meetwaarden[0]; #de init waarde van max is de eerste plek in de array
   
 for x in range(99):#De for loop doorloopt de volledige array
    
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
 print(maxWaarde, topwaarde_werkelijk, effectiefgemeten_spanning);


    
spanning_meten()
stroom_meten()