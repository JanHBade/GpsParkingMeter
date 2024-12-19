# Install

## DNSMasq (DHCP Server)

sudo apt install dnsmasq

sudo nmtui -> Alle Verbindungen löschen

/etc/dnsmasq.conf
```
# Listen on this specific port instead of the standard DNS port
# (53). Setting this to zero completely disables DNS function,
# leaving only DHCP and/or TFTP.
port=0

interface=wlan0
dhcp-authoritative
dhcp-leasefile=/tmp/dhcp.leases
dhcp-range=10.0.0.2,10.0.0.10,24h
#subnet mask
dhcp-option=1,255.0.0.0

# Do not send gateway to client
dhcp-option=3
# Disable DNS
dhcp-option=6
```

## WPA Supplicant (WLan Verwaltung)

/etc/wpa_supplicant/wpa_supplicant.conf
```
ctrl_interface=DIR=/var/run/wpa_supplicant

network={
    ssid="yourSSID"
    key_mgmt=WPA-PSK
    psk="yourpasscode"
    priority=1
    id_str="dhcp_client"
}

network={
    ssid="Hotspot"
    mode=2
    key_mgmt=WPA-PSK
    psk="password"
    frequency=2437
    id_str="dhcp_server"
}
```

## Netzwerk Einstellungen

/etc/network/interfaces
```
auto lo
iface lo inet loopback

auto wlan0
iface wlan0 inet manual
  wpa-driver nl80211
  wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

iface dhcp_server inet static
  address 10.0.0.1
  netmask 255.0.0.0

iface dhcp_client inet dhcp
```
