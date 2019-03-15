# lampa
switch something off or on. like lampa

use mqtt server and RPi2

## common command to install:
```
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
rm -f mosquitto-repo.gpg.key
echo "deb https://repo.mosquitto.org/debian stretch main" | sudo tee /etc/apt/sources.list.d/mosquitto-stretch.list
sudo apt-get update
sudo apt-get -y install python3-pip mosquitto mosquitto-clients
cd ~/lampa/
pip3 install -r requirements.txt
sudo cp lampa.service /etc/systemd/system/
sudo systemctl daemon-reload 
sudo systemctl enable lampa.service
sudo systemctl start lampa.service
sudo systemctl status lampa.service

```

[![Build Status](https://travis-ci.org/ryabukha/lampa.svg?branch=master)](https://travis-ci.org/ryabukha/lampa)

## control...
sudo systemctl start/stop/status lampa.service

## links:

- [mqtt server install](http://robot-on.ru/articles/ystanovka-mqtt-brokera-mosquitto-raspberry-orange-pi)
- [paho python client](https://www.eclipse.org/paho/clients/python/)
