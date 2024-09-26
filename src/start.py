#!/usr/bin/python3

import logging
logging.basicConfig(level=logging.DEBUG)

from gpiozero import LED
import time,datetime
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in13_V4
import gpsd

red = LED(4)
green = LED(27)
yellow = LED(22)

#font = ImageFont.truetype("/usr/share/fonts/opentye/freefont/FreeMono.otf", 96)
font = ImageFont.truetype("./RobotoCondensed.ttf", 110)

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

    try:
        #while True:
        logging.info("Connect to the local gpsd")
        gpsd.connect()

        logging.info("Get gps position")
        packet = gpsd.get_current()

        logging.info("Get Local Time")
        ltime = packet.get_time(local_time=True)
        logging.info("Time: " + str(ltime))

        logging.info("init ePaper")
        epd.init()
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle([(0,0),(epd.height, epd.width)],outline = 0, width = 2, radius = 5)
        #draw.rectangle([(0,0),(50,50)],outline = 0)
        #draw.rectangle([(55,0),(100,50)],fill = 0)
        draw.text((0, 0), ltime.strftime("%H:%M"), font = font, fill = 0)
        logging.info("display image")
        epd.display(epd.getbuffer(image))

        #time.sleep(10)
    except KeyboardInterrupt:
        print("Keyboard Abbruch")