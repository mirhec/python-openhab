#!/usr/bin/env python
import datetime
import openhab
from openhab import Item
from time import sleep
import RPi.GPIO as GPIO

if __name__ == '__main__':
    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)

    # Pin 18 (GPIO 24) auf Input setzen
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)

    while 1:
        try:
            base_url = 'http://openhab:8080/rest'

            # fetch all items
            items = openhab.fetch_all_items(base_url)

            # define items
            temps = [
                {
                    'soll': 'Temp_EG_Wohnzimmer_soll', 
                    'ist': 'Temp_EG_Wohnzimmer_akt',
                    'switch': 'Heat_Wohnzimmer',
                    'gpio': 3
                }, 
                {
                    'soll': 'Temp_EG_Kueche_soll', 
                    'ist': 'Temp_EG_Kueche_akt',
                    'switch': 'Heat_Kueche',
                    'gpio': 5
                }, 
                {
                    'soll': 'Temp_EG_Arbeitszimmer_soll', 
                    'ist': 'Temp_EG_Arbeitszimmer_akt',
                    'switch': 'Heat_Arbeitszimmer',
                    'gpio': 7
                }, 
                {
                    'soll': 'Temp_EG_Klo_soll', 
                    'ist': 'Temp_EG_Klo_akt',
                    'switch': 'Heat_Klo',
                    'gpio': 8
                }
            ]

            # get temp item
            while 1:
                for temp in temps:
                    soll = items.get(temp['soll'])
                    ist = items.get(temp['ist'])
                    switch = items.get(temp['switch'])
                    if ist.state <= soll.state - 1 and switch.state != 'ON':
                        switch.state = 'ON'
                        print('Enabled heating for %s' % switch.name)
                    
                    if ist.state >= soll.state + 1 and switch.state != 'OFF':
                        switch.state = 'OFF'
                        print('Disabled heating for %s' % switch.name)
                    
                    if(switch.state == 'ON'):
                        # set switch ON
                        GPIO.output(temp['gpio'], GPIO.HIGH)
                    else:
                        # set switch off
                        GPIO.output(temp['gpio'], GPIO.LOW)
                sleep(1)
        except:
            print('Error occured, try again!')