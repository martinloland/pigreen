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

## Start server

export FLASK_APP=server.py

flask run