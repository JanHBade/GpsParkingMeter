#!/usr/bin/python3

import time,datetime,sys
from PIL import Image,ImageDraw,ImageFont

import logging
import logging.handlers as handlers
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s|%(name)s|%(levelname)s|%(message)s",
    handlers=[
        handlers.RotatingFileHandler('GpsParkingMeter.log', maxBytes=5_000_000, backupCount=3),
        logging.StreamHandler(sys.stdout)
    ]
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)
logging.getLogger('waveshare_epd.epd2in13_V4').setLevel(logging.INFO)


from waveshare_epd import epd2in13_V4

MAX_FONT_SIZE = 160
font = ImageFont.truetype("./digital-7.ttf", MAX_FONT_SIZE)
fontOled = ImageFont.truetype("/usr/share/fonts/opentye/freefont/FreeMono.otf", 14)

oldtime = datetime.datetime(2002, 9, 27, 14, 30, 0)

def updateEInk(text_to_display):
    logging.info("Find Font Size")
    fontsize = MAX_FONT_SIZE
    global font
    font = font.font_variant(size=fontsize)
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
    left = (epd.height - text_dim[2]) / 2
    logging.debug("left: " + str(left))
    logging.debug("text: " + text_to_display)
    draw.text((left, -10), text_to_display, font = font, fill = 0)
    logging.info("display image")
    epd.display(epd.getbuffer(image))

if __name__ == "__main__":
    logging.info("Start")

    epd = epd2in13_V4.EPD()
    logging.info("Epaper H: " + str(epd.height) + " W: " + str(epd.width))

    try:
        while True:
            ltime = datetime.datetime.now()
            logging.info("Local Time: " + str(ltime))

            diff = ltime - oldtime
            if diff > datetime.timedelta(minutes=40):
                if ltime.minute < 30:
                    textEink = str(ltime.hour) + ":30"
                else:
                    textEink = str( (ltime+datetime.timedelta(hours=1)).hour ) + ":00"
                
                logging.info("Eink Time (Startup oder Diff): " + textEink)
                updateEInk(textEink)
                oldtime = ltime
            
            if ltime.minute == 1:
                textEink = str(ltime.hour) + ":30"
                logging.info("Eink Time: " + textEink)
                updateEInk(textEink)
                oldtime = ltime
            elif ltime.minute == 31:
                textEink = str( (ltime+datetime.timedelta(hours=1)).hour ) + ":00"
                logging.info("Eink Time: " + textEink)
                updateEInk(textEink)
                oldtime = ltime

            time.sleep(58)
    except KeyboardInterrupt:
        print("Keyboard Abbruch")

    logging.info("Goto Sleep...")
    epd.sleep()
