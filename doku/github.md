
## Zugriff über SSH

Github_id_rsa auf pi kopieren (aus Keys Ordner)

```
chmod 0600 Github_id_rsa
ssh -i ./Github_id_rsa -T git@github.com
```

remote over ssh hinzufügen
im GpsParkingMeter Ordner
```
git remote add ssh git@github.com:JanHBade/GpsParkingMeter.git
git config core.sshCommand 'ssh -i private_key_file' 
```
