#!/usr/bin/env python
import datetime
import openhab
from openhab import Item
from time import sleep

if __name__ == '__main__':
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
                    'switch': 'Heat_Wohnzimmer'
                }, 
                {
                    'soll': 'Temp_EG_Kueche_soll', 
                    'ist': 'Temp_EG_Kueche_akt',
                    'switch': 'Heat_Kueche'
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
                sleep(1)
        except:
            print('Error occured, try again!')