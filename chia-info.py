from enum import Enum
from logging import exception
from pickle import TRUE
from time import sleep
import PySimpleGUI as sg
import shutil as sh
import requests
import getopt
import json
import datetime

# Parameters TODO: Please replace the address below with your own Chia Receive address
wallet_address = 'xch1ympws6g96jkwwl6t3qvl7klz8k9nlrru9htux7ulq6a3ha8surnqndcaxl';

# Globals
window = None;
graph_coins = None;
graph_value = None;
coins_rect = None;
coins_text = None;
value_rect = None;
value_text = None;
MSG_COINS = 0.00;
MSG_VALUE = 0.00;
MSG_PRICE = 0.00;

# Constants
WINDOW_SIZE = 360;
BAR_WIDTH = WINDOW_SIZE;
GRAPH_SIZE = (WINDOW_SIZE,100);
FONT = 'Times 48 bold ';
FONT_PRICE = 'Times 22 bold ';

# Main
while True:
  
    coins = 0;
    coinValue = 0;

    try:
        # Pull Info from WebService
        coins =requests.get('https://xchscan.com/api/account/balance?address=%s' % wallet_address).json()
        coinValue =requests.get('https://xchscan.com/api/chia-price').json()

        if not ((type(coins) == float) and (type(coins) == float)):
            raise Exception("Unexpected data from XCHSCAN"); 

        # Message Construction
        MSG_COINS = "%.2f XCH" % coins['xch']
        MSG_VALUE = "$%.2f USD" % float((coinValue['usd'] * coins['xch']))
        MSG_PRICE = "Current Price: $%.2f USD" % float(coinValue['usd'])
    
    except Exception as ex:
        dt = datetime.datetime.now();
        timestamp = '%s-%s-%s' % (dt.hour, dt.minute, dt.second);
        print('[%s]' % timestamp + " - XCHSCAN Error: " + ex.msg);
    finally:
        print('[%s]' % timestamp + " - Waiting 20 Minutes until we hit the service again...");
        sleep(12000);
        continue;
            
    if window == None: 
            
            # Window & Graph Setup
            graph_price = sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='GRAPH-PRICE')
            graph_coins = sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='GRAPH-COINS')
            graph_value = sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key='GRAPH-VALUE')
            layout = [[graph_price],[graph_coins],[graph_value]]    
            window = sg.Window('My Chia Wallet & Current Price', layout, finalize=True)
                   
    else:
            
             # Delete Coins Graph Data
            graph_price.delete_figure(price_rect)
            graph_price.delete_figure(price_text)

            # Delete Coins Graph Data
            graph_coins.delete_figure(coins_rect)
            graph_coins.delete_figure(coins_text)
            
             # Delete Value Graph Data
            graph_value.delete_figure(value_rect)
            graph_value.delete_figure(value_text)
    
    
    # (Re)Create Price Graph
    price_rect = graph_price.DrawRectangle(top_left=(0, 100), bottom_right=(BAR_WIDTH, 0), fill_color='#ffffff')
    price_text = graph_price.DrawText(font=FONT_PRICE,text=MSG_PRICE, location=(BAR_WIDTH / 2, 100/2))

    # (Re)Create Coins Graph
    coins_rect = graph_coins.DrawRectangle(top_left=(0, 100), bottom_right=(BAR_WIDTH, 0), fill_color='#009933')
    coins_text = graph_coins.DrawText(font=FONT, text=MSG_COINS, location=(BAR_WIDTH / 2, 100/2))

    # (Re)Create Value Graph
    value_rect = graph_value.DrawRectangle(top_left=(0, 100), bottom_right=(BAR_WIDTH, 0), fill_color='#ff8000')
    value_text = graph_value.DrawText(font=FONT,text=MSG_VALUE, location=(BAR_WIDTH / 2, 100/2))

    while True:
        event, values = window.Read(20000)
        break
    