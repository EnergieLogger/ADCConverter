# Imports voor OLED
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import RPi.GPIO as GPIO
# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.
GPIO.setwarnings(False)

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Setting up OLED !!!
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

disp.begin()
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

state = 1

def change_state(channel):
    global state
    if state == 1:
        state = 2
    else:
        state = 1

def display_info(spanning, stroom, vermogen, cosphi, verbruik, state):

    if state == 1:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Write two lines of text.

        draw.text((x, top),       "Spanning: " + str(spanning) + "V",  font=font, fill=255)
        draw.text((x, top+8),     "Stroom: " + str(stroom)+ "A", font=font, fill=255)
        draw.text((x, top+16),    "Vermogen: " + str(vermogen)+ "kW",  font=font, fill=255)
        draw.text((x, top+24),    "Cosphi: " + str(cosphi)+ "p.u.",  font=font, fill=255)
        draw.text((x, top+32),    "Verbruik: " + str(vermogen)+ "kWh",  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.1)
    elif state == 2:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Write two lines of text.
        draw.text((x, top),    "Verbruik: " + str(vermogen)+ "kWh",  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.1)


# Zet de GPIO pin als ingang.
GPIO.setup(22, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
# Gebruik een interrupt, wanneer actief run subroutinne 'gedrukt'




GPIO.add_event_detect(22, GPIO.RISING, callback=change_state, bouncetime=200)

while True:
    display_info(230,10,2300, 0.96, 25, state)
    time.sleep(.1)

