# pigreen
Greenhouse front and backend on raspberry pi

## System configuration

* enable ssh and serial
* turn off UI boot
* configure static ip
  https://www.circuitbasics.com/how-to-set-up-a-static-ip-on-the-raspberry-pi/
* make folder *scripts* inside home
* change default python https://raspberry-valley.azurewebsites.net/Python-Default-Version/
* git clone repo

## Virtualenv

`sudo pip3 install virtualenv virtualenvwrapper=='4.8.4'`

```
nano ~/.bashrc # and add:

VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
export PATH=/usr/local/bin:$PATH
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

source ~/.bashrc
```

You can now use mkvirtualenv

## DHT

https://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/


## Rpi.GPIO

`sudo apt-get -y install python3-rpi.gpio`

## Screen

https://raspi.tv/2012/using-screen-with-raspberry-pi-to-avoid-leaving-ssh-sessions-open

`sudo apt-get install screen`

Start new: `screen bash`

Detach: `CTRL + A` then `D`

View: `screen -list`

Reconnect: `screen -r 1245.pts-0.raspberrypi`

Terminate: `CTRL + D`

## Start server

`sudo flask run -h 0.0.0.0 -p 80`

## Start manager

`sudo python manager.py`

## WiFi Strength

` sudo iwlist wlan0 scan | egrep "Cell|ESSID|Signal|Rates"`