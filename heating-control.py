#!/usr/bin/env python
import datetime
import openhab
from openhab import Item
from time import sleep
import RPi.GPIO as GPIO

if __name__ == '__main__':
    ###### BEGIN EDIT SECTION
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
    ###### END EDIT SECTION

    # Use RPi.GPIO layout (pin numbering)
    # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Setup pins
    print('Setup pins ... ')
    for gpio in [8, 10, 12, 16, 18, 22, 24, 26]:
        print('  -> pin %s as output' % gpio)
        GPIO.setup(gpio, GPIO.OUT)
        sleep(.1)
        # print('switch on pin %s' % gpio)
        GPIO.output(gpio, GPIO.LOW) # set switch on (relais are inverted)
        sleep(.1)
        # print('switch off pin %s' % gpio)
        GPIO.output(gpio, GPIO.HIGH) # set switch off (relais are inverted)
    print('done.')

    while 1:
        try:
            print("I'm up and running ...")
            
            base_url = 'http://openhab:8080/rest'

            # fetch all items
            items = openhab.fetch_all_items(base_url)

            # get temp item
            while 1:
                for temp in temps:
                    soll = items.get(temp['soll'])
                    ist = items.get(temp['ist'])
                    switch = items.get(temp['switch'])
                    
                    if ist.state < soll.state and switch.state != 'ON':
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
        except KeyboardInterrupt:
            raise
        except:
            print('Error occured, try again!')
