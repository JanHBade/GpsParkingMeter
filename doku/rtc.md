# RTC

sudo raspi-config -> Interfacing Options -> I2C -> Yes

sudo apt install python3-smbus i2c-tools

sudo i2cdetect -y 1

UU -> in Nutzung

sudo nano /boot/config.txt
```
dtoverlay=i2c-rtc,ds3231
```

```
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock
```

sudo nano /lib/udev/hwclock-set 
```
#!/bin/sh
# Reset the System Clock to UTC if the hardware clock from which it
# was copied by the kernel was in localtime.

dev=$1

#if [ -e /run/systemd/system ] ; then
#    exit 0
#fi

#/sbin/hwclock --rtc=$dev --systz
#/sbin/hwclock --rtc=$dev --hctosys
```

## Check

sudo hwclock -v
