# Install

sudo apt install pps-tools

# Config

## /boot/firmware/config.txt 

Schaltplan und pinout.xyz gucken welcher das ist (GPIO)
```
dtoverlay=pps-gpio,gpiopin=23
```

## /etc/modules
```
pps-gpio
```

## Test

sudo ppstest /dev/pps0
