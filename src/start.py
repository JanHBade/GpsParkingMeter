#!/usr/bin/python3

import gpsd

# Connect to the local gpsd
gpsd.connect()

# Get gps position
packet = gpsd.get_current()

# See the inline docs for GpsResponse for the available data
print(packet.position())

print(packet.get_time())
print(packet.get_time(local_time=True))