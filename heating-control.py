#!/usr/bin/env python
import datetime
import openhab
from openhab import Item
from time import sleep
import RPi.GPIO as GPIO

if __name__ == '__main__':
    # define temp items
    temps = [
        {
            'soll': 'Temp_EG_Wohnzimmer_soll', 
            'ist': 'Temp_EG_Wohnzimmer_akt',
            'switch': 'Heat_Wohnzimmer',
            'gpio': [22, 24, 26]
        }, 
        {
            'soll': 'Temp_EG_Kueche_soll', 
            'ist': 'Temp_EG_Kueche_akt',
            'switch': 'Heat_Kueche',
            'gpio': [8]
        }, 
        {
            'soll': 'Temp_EG_Arbeitszimmer_soll', 
            'ist': 'Temp_EG_Arbeitszimmer_akt',
            'switch': 'Heat_Arbeitszimmer',
            'gpio': [10]
        }, 
        {
            'soll': 'Temp_EG_Klo_soll', 
            'ist': 'Temp_EG_Klo_akt',
            'switch': 'Heat_Klo',
            'gpio': [12]
        }
    ]

    # Use RPi.GPIO layout (pin numbering)
    GPIO.setmode(GPIO.BOARD)

    # Setup pins
    for t in temps:
        for gpio in t['gpio']:
            GPIO.setup(gpio, GPIO.OUT)

    while 1:
        try:
            base_url = 'http://openhab:8080/rest'

            # fetch all items
            items = openhab.fetch_all_items(base_url)

            # get temp item
            while 1:
                for temp in temps:
                    soll = items.get(temp['soll'])
                    ist = items.get(temp['ist'])
                    switch = items.get(temp['switch'])
                    
                    if ist.state <= soll.state - .5 and switch.state != 'ON':
                        switch.state = 'ON'
                        print('Enabled heating for %s' % switch.name)
                    
                    if ist.state >= soll.state + .5 and switch.state != 'OFF':
                        switch.state = 'OFF'
                        print('Disabled heating for %s' % switch.name)
                    
                    if(switch.state == 'ON'):
                        # set switch ON
                        for gpio in temp['gpio']:
                            GPIO.output(gpio, GPIO.LOW)
                    else:
                        # set switch off
                        for gpio in temp['gpio']:
                            GPIO.output(gpio, GPIO.HIGH)
                sleep(1)
        except:
            print('Error occured, try again!')