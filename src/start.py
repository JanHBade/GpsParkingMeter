#!/usr/bin/python3


import time,datetime,sys
from gpiozero import LED
from PIL import Image,ImageDraw,ImageFont

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.core.virtual import terminal
from luma.oled.device import ssd1306

import logging
import logging.handlers as handlers
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        handlers.RotatingFileHandler('GpsParkingMeter.log', maxBytes=500_000, backupCount=3),
        logging.StreamHandler(sys.stdout)
    ]
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)
logging.getLogger('gpsd').setLevel(logging.ERROR)
logging.getLogger('waveshare_epd.epd2in13_V4').setLevel(logging.INFO)


from waveshare_epd import epd2in13_V4
import gpsd

red = LED(4)
green = LED(27)
yellow = LED(22)

#in km/h
min_speed = 10

MAX_FONT_SIZE = 160
font = ImageFont.truetype("./digital-7.ttf", MAX_FONT_SIZE)
fontOled = ImageFont.truetype("/usr/share/fonts/opentye/freefont/FreeMono.otf", 14)

oldtime = datetime.datetime(2002, 9, 27, 14, 30, 0).astimezone()

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
term = terminal(device, fontOled, animate=False)

OledShift = 0
def updateOled(text_to_display):
    global OledShift    
    oledtext = "\n" + " " * OledShift + text_to_display
    OledShift = OledShift + 1                    
    if OledShift == 3:
        OledShift = 0
        term.reverse_colors()
    term.puts(oledtext)

if __name__ == "__main__":
    logging.info("init LEDs")
    red.on()
    time.sleep(0.2)
    green.on()
    time.sleep(0.2)
    yellow.on()
    time.sleep(0.2)
    red.off()
    green.off()
    yellow.off()

    epd = epd2in13_V4.EPD()
    logging.info("Epaper H: " + str(epd.height) + " W: " + str(epd.width))

    try:
        while True:
            logging.info("Connect to the local gpsd and get GPS Data")
            gpsd.connect()
            packet = gpsd.get_current()

            if packet.mode > 2:     #3d Fix needed for speed
                green.on()
                yellow.off()
                ltime = packet.get_time(local_time=True)
                text_to_display = ltime.strftime("%H:%M")
                logging.info("Local Time: " + str(ltime))

                logging.debug(packet.error)

                if oldtime == ltime:
                    logging.warning("GPS time stands still")
                
                pos = packet.position()
                speed = packet.speed()

                logging.info("Update OLED")
                updateOled(text_to_display + f" {speed:.1f}")

                # speed in m/s, min_speed in km/h
                if speed > (min_speed / 3.6):   #wir bewegen uns
                    if (ltime - oldtime).total_seconds() > 60:
                        oldtime = ltime
                        
                        logging.info("Find Font Size")
                        fontsize = MAX_FONT_SIZE
                        text_dim = font.getbbox(text_to_display)
                        while text_dim[2] > (epd.height-5) or text_dim[3] > epd.width:
                            fontsize -= 1
                            font = font.font_variant(size=fontsize)
                            text_dim = font.getbbox(text_to_display)

                        logging.info("New Font Size: " + str(fontsize))

                        logging.info("init ePaper")
                        epd.init()
                        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
                        draw = ImageDraw.Draw(image)
                        draw.rounded_rectangle([(0,0),(epd.height, epd.width)],outline = 0, width = 2, radius = 5)
                        draw.text((0, -10), text_to_display, font = font, fill = 0)
                        logging.info("display image")
                        epd.display(epd.getbuffer(image))    
                else:
                    logging.info("to slow no update")                                    
            else:
                yellow.on()
                green.off()
                updateOled("No GPS: " + str(packet.mode))
                logging.warning("No GPS: " + str(packet.mode))

            time.sleep(2)
    except KeyboardInterrupt:
        red.on()
        green.off()
        yellow.off()
        print("Keyboard Abbruch")

    logging.info("Goto Sleep...")
    epd.sleep()
