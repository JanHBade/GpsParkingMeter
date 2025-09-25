# /etc/ssh/sshd_config

Weniger Lags über WLAN
```
UseDNS no
IPQoS throughput
```

Anmeldung über Zertifikat
```
PubkeyAuthentication yes
AuthorizedKeysFile      .ssh/authorized_keys .ssh/authorized_keys2
```
Dann Zertifikat unter der Datei ablegen (.ssh/authorized_keys)
