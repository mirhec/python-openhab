Heat-Controlling script
============
  This script is based on the library forked from https://github.com/sim0nx/python-openhab and
  is intended to be executed on a raspberry pi. You can parameterize the GPIOs that should be
  set based on the actual and destination temperature in the rooms.

Installation
------------
  - `sudo apt-get update`
  - `sudo apt-get install git python-dev python-pip python-rpi.gpio`
  - `git clone git://git.drogon.net/wiringPi`
  - `cd wiringPi`
  - `./build`
  - `cd ..`
  - `git clone https://github.com/mirhec/python-openhab`
  - `cd python-openhab`
  - `sudo pip install -r requirements.txt`
  - Check if the script is working: `python heating-control.py`
  - Create the file /etc/systemd/system/heating-control.service with the following contents:
```bash
[Unit]
Description=Heating control script
After=network-online.target
Wants=network-online.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/python-openhab/heating-control.py

[Install]
WantedBy=multi-user.target
```
  - `sudo chmod 644 /etc/systemd/system/heating-control.service`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable heating-control.service`
  - `sudo systemctl start heating-control.service`
  - Then check for the service status: `sudo systemctl status heating-control`
  - Now you can configure the script by editing it
