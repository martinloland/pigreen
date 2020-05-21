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

sudo pip3 install virtualenv virtualenvwrapper=='4.8.4'

nano ~/.bashrc # and add:

VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
export PATH=/usr/local/bin:$PATH
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

source ~/.bashrc

You can now use mkvirtualenv

## Start server

export FLASK_APP=server.py

flask run