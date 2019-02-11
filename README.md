# lampa
switch something off or on. like lampa

use mqtt server and RPi2

## common command to install:
```
sudo wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
rm -f mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
sudo wget http://repo.mosquitto.org/debian/mosquitto-stretch.list
sudo apt-get update
sudo apt-get -y install python3-pip mosquitto mosquitto-clients
cd ~
pip3 install paho-mqtt
pip3 install RPi.GPIO
cd ./lampa/
mkdir logs
sudo cp lampa.sh /etc/init.d
sudo update-rc.d lampa.sh defaults
```

## control...
sudo /etc/init.d/lampa.sh star/stop/status

## links:

- [mqtt server install](http://robot-on.ru/articles/ystanovka-mqtt-brokera-mosquitto-raspberry-orange-pi)
- [paho python client](https://www.eclipse.org/paho/clients/python/)
- [getting a python script to run in the background](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/)

hello slack
start
