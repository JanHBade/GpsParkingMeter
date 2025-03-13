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
        handlers.RotatingFileHandler('GpsParkingMeter.log', maxBytes=5_000_000, backupCount=3),
        logging.StreamHandler(sys.stdout)
    ]
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)
logging.getLogger('waveshare_epd.epd2in13_V4').setLevel(logging.INFO)


from waveshare_epd import epd2in13_V4

red = LED(4)
green = LED(27)
yellow = LED(22)

MAX_FONT_SIZE = 160
font = ImageFont.truetype("./digital-7.ttf", MAX_FONT_SIZE)
fontOled = ImageFont.truetype("/usr/share/fonts/opentye/freefont/FreeMono.otf", 14)

oldtime = datetime.datetime(2002, 9, 27, 14, 30, 0)

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

def updateEInk(text_to_display):
    logging.info("Find Font Size")
    fontsize = MAX_FONT_SIZE
    global font
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
        ltime = datetime.datetime.now()
        if ltime.minute < 30:
            textEink = str(ltime.hour) + ":30"
        else:
            textEink = str( (ltime+datetime.timedelta(hours=1)).hour ) + ":00"

        logging.info("Eink Time (Startup): " + textEink)
        updateEInk(textEink)

        while True:
            green.on()

            ltime = datetime.datetime.now()

            text_to_display = ltime.strftime("%H:%M:%S")
            logging.info("Local Time: " + str(ltime))
            
            logging.info("Update OLED")
            updateOled(text_to_display)

            if ltime.minute == 1:
                yellow.on()
                textEink = str(ltime.hour) + ":30"
                logging.info("Eink Time: " + textEink)
                updateEInk(textEink)
            elif ltime.minute == 31:
                yellow.on()
                textEink = str( (ltime+datetime.timedelta(hours=1)).hour ) + ":00"
                logging.info("Eink Time: " + textEink)
                updateEInk(textEink)
            else:
                yellow.off()

            time.sleep(58)
    except KeyboardInterrupt:
        red.on()
        green.off()
        yellow.off()
        print("Keyboard Abbruch")

    logging.info("Goto Sleep...")
    epd.sleep()
