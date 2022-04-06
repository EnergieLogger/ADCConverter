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
indexWaarde = 0;
indexWaardeS = 0;
def meten():

 for x in range(99): #array vullen met meetwaarden dmv for loop

  meetwaarden.insert(x, chan.voltage); #omrekening van analoge waarde naar spanning (dus *3.3V)

  maxWaarde = meetwaarden[0]; #de init waarde van max is de eerste plek in de array

  meetwaardenstroom.insert(x, chanstroom.voltage);

  maxWaardeStroom = meetwaardenstroom[0]

 for x in range(99):#De for loop doorloopt de volledige array

    if(maxWaarde < meetwaarden[x]): #als de volgende array kleiner is dan max was dan krijgt max een nieuwe waarde.

        maxWaarde = meetwaarden[x];
        indexWaarde = x;
    if(maxWaardeStroom < meetwaardenstroom[x]):
        indexWaardeS = x;
        maxWaardeStroom = meetwaardenstroom[x];
 Timer(1, meten).start() #iedere seconde wordt de functie voor het meten van de spanning aangeroepen

 topwaarde_werkelijkStroom = (maxWaardeStroom - 1.671)*10;
 topwaarde_werkelijk = maxWaarde *144.4; #de werkelijke waarde van de spanning is de max spanning keer een versterkingsfactor
 effectiefgemeten_spanning = topwaarde_werkelijk*0.707; #om van topwaarde naar effectief te gaan wordt vermenigvuldigt met 0,5wortel2 (0,7071)
 data = {

     'Topwaarde spanning': maxWaarde,
     'Topwaarde werkelijk': topwaarde_werkelijk,
     'Effectief gemeten spanning': effectiefgemeten_spanning,
     'Stroom': topwaarde_werkelijkStroom
 }
 json_string = json.dumps(data)
 with open('json_data.json', 'w') as outfile:
    json.dump(json_string, outfile)
 with open('json_data.json') as json_file:
    data = json.load(json_file)
    print(data)
 print("\n",maxWaarde,"\n", topwaarde_werkelijk,"\n", effectiefgemeten_spanning);
 print(topwaarde_werkelijkStroom, "A")
 print("\nde Index waarde van de spanning bevindt zich op positie:", indexWaarde)
 print("\nde Index waarde van de stroom bevindt zich op positie:", indexWaardeS)


meten()

