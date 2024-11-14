# Install

sudo raspi-config -> Interfacing Options -> I2C -> Yes

/boot/firmware/config.txt
```
dtparam=i2c_arm=on
```

sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 python3-luma.oled i2c-tools