
/etc/systemd/system/GpsPM.service

(liegt auch im src Verszeichnis, dann link dahin erstellen)

```
[Unit]
Description=GPS Parking Meter
After=syslog.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/GpsParkingMeter/src
ExecStart=/home/pi/GpsParkingMeter/src/start.py

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload

systemctl enable GpsPM

systemctl start GpsPM