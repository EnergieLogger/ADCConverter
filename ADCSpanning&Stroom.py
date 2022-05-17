import sched, time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from threading import Timer
import json
import math

import RPi.GPIO as GPIO
from OLED import display_info
from OLED import change_state

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.
GPIO.setwarnings(False)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
rate = 860


# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)


# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
chanstroom = AnalogIn(ads, ADS.P1)
meetwaarden = [0]*10
meetwaardenstroom = [0]*10;
indexWaarde = 0;
indexWaardeS = 0;
cosphiU = 0;
cosphiA = 0;
cosphi = 0;
cosphitotaal =0;
cosphiWerkelijk =0;
verbruiktotaal = 0;
ads.data_rate = rate
verbruik = 0;

state = 1

# Zet de GPIO pin als ingang.
GPIO.setup(22, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
# Gebruik een interrupt, wanneer actief run subroutinne 'gedrukt'
GPIO.add_event_detect(22, GPIO.RISING, callback=change_state, bouncetime=200)

def stateveranderen():
 global state

 if(state ==1):
     state = 2
 else:
   state = 1
 Timer(3, stateveranderen).start()
def meten():
 global indexWaarde;
 global indexWaardeS;
 global cosphiWerkelijk;
 global verbruiktotaal;
 global verbruik;
 
 for x in range(16): #array vullen met meetwaarden dmv for loop

  meetwaarden.insert(x, chan.voltage); #omrekening van analoge waarde naar spanning (dus *3.3V)

  maxWaarde = meetwaarden[0]; #de init waarde van max is de eerste plek in de array

  meetwaardenstroom.insert(x, chanstroom.voltage);

  maxWaardeStroom = meetwaardenstroom[0]

 for x in range(16):#De for loop doorloopt de volledige array

    if(maxWaarde < meetwaarden[x]): #als de volgende array kleiner is dan max was dan krijgt max een nieuwe waarde.

        maxWaarde = meetwaarden[x];
        indexWaarde = x;
    if(maxWaardeStroom < meetwaardenstroom[x]):
        indexWaardeS = x;
        maxWaardeStroom = meetwaardenstroom[x];
 

 topwaarde_werkelijkStroom = round((maxWaardeStroom - 1.665)*10,3);
 topwaarde_werkelijk =round(( maxWaarde *144.4),2); #de werkelijke waarde van de spanning is de max spanning keer een versterkingsfactor
 effectiefgemeten_spanning = round((topwaarde_werkelijk*0.707),2); #om van topwaarde naar effectief te gaan wordt vermenigvuldigt met 0,5wortel2 (0,7071)
 effectiefgemeten_stroom = round((topwaarde_werkelijkStroom*0.707),2);
 cosphiU = indexWaarde*(1/475)
 cosphiA = indexWaardeS*(1/475)
 cosphitotaal = (cosphiU - cosphiA)/0.02
 cosphiC = cosphitotaal *360
 cosphi =abs(round( math.cos(cosphiC),2))
 if (cosphi < 0.2):
   cosphiWerkelijk = 1 - cosphi;
 else:
   cosphiWerkelijk = cosphi;
 Timer(1, meten).start()  
 effectiefVermogen = round(((effectiefgemeten_spanning * effectiefgemeten_stroom * cosphiWerkelijk)),1);
 effectiefVermogenTot =  round(((effectiefVermogen/1000)),2);
 if(topwaarde_werkelijkStroom > 0.01):
   verbruik = effectiefVermogenTot

 verbruiktotaal = verbruiktotaal + verbruik;




 data = {

     'Topwaarde spanning': maxWaarde,
     'Topwaarde werkelijk': topwaarde_werkelijk,
     'Effectief gemeten spanning': effectiefgemeten_spanning,
     'Stroom': topwaarde_werkelijkStroom,
     'Verbruik': verbruiktotaal,
     'Vermogen': effectiefVermogen,
     'Tijd': time.time(),
     'CosPhi': cosphiWerkelijk
 }
 currdata = []
 with open('/var/www/html/assets/json_data.json', 'r') as json_file:
  try:
    data1 = json.load(json_file)
    currdata = data1["Data"]
  except:
    print()

 currdata.append(data)
 #json_file["data"].append
 with open('/var/www/html/assets/json_data.json', 'w') as json_file:
    json_file.write(json.dumps({"Data": currdata}))
 print("\n",maxWaarde,"\n", topwaarde_werkelijk,"\n", effectiefgemeten_spanning);
 print(topwaarde_werkelijkStroom, "A")
#print("\nde Index waarde van de spanning bevindt zich op positie:", indexWaarde)
#print("\nde Index waarde van de stroom bevindt zich op positie:", indexWaardeS)
 print("\nde Cosphi is:", cosphiWerkelijk)
 print("\nVermogen: ", effectiefVermogenTot, " kW")
 print("\nVerbruik: ", verbruiktotaal, " kWh")


 display_info(effectiefgemeten_spanning,topwaarde_werkelijkStroom, effectiefVermogen, cosphiWerkelijk, verbruiktotaal, state)



meten();
stateveranderen();  

