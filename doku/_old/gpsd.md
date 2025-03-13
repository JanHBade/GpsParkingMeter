# Install

sudo apt install gpsd gpsd-clients

# /etc/defaults/gpsd
```
# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyS0 /dev/pps0"

# Other options you want to pass to gpsd
GPSD_OPTIONS="-Gn"

# Automatically hot add/remove USB GPS devices via gpsdctl
USBAUTO="true"
```

#  /lib/systemd/system/gpsd.socket
```
[Unit]
Description=GPS (Global Positioning System) Daemon Sockets

[Socket]
ListenStream=/run/gpsd.sock
ListenStream=[::1]:2947
#ListenStream=127.0.0.1:2947
# To allow gpsd remote access, start gpsd with the -G option and
# uncomment the next two lines:
#ListenStream=[::1]:2947
ListenStream=0.0.0.0:2947
SocketMode=0600
#BindIPv6Only=yes

[Install]
WantedBy=sockets.target
```