# RTC

sudo raspi-config -> Interfacing Options -> I2C -> Yes

sudo apt install python3-smbus i2c-tools

sudo nano /boot/firmware/config.txt
```
dtoverlay=i2c-rtc,ds3231
```
sudo i2cdetect -y 1
UU -> in Nutzung

## Prüfung

timedatectl status
``` 
               Local time: Mo 2026-09-21 10:24:13 BST
           Universal time: Mo 2026-09-21 09:24:13 UTC
                 RTC time: Mo 2026-09-21 09:24:13
                Time zone: Europe/London (BST, +0100)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```
