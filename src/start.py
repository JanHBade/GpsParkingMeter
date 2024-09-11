#!/usr/bin/python3

from gpiozero import LED
import time,datetime

import gpsd

red = LED(4)
green = LED(27)
yellow = LED(22)

if __name__ == "__main__":
    red.on()
    time.sleep(0.2)
    green.on()
    time.sleep(0.2)
    yellow.on()
    time.sleep(0.2)
    red.off()
    green.off()
    yellow.off()

    try:
        while True:
            # Connect to the local gpsd
            gpsd.connect()

            # Get gps position
            packet = gpsd.get_current()

            ltime = packet.get_time(local_time=True)
            #print(ltime)

            time.sleep(10)
    except KeyboardInterrupt:
        print("Keyboard Abbruch")