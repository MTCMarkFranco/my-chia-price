from enum import Enum
from pickle import TRUE
import PySimpleGUI as sg
import shutil as sh
import requests
import getopt

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
CHIA_PRICE = 0.00;

# Main
while True:
  
    coins = 0;
    coinValue = 0;

    try:
        # Pull Info from WebService
        coins =requests.get('https://xchscan.com/api/account/balance?address=%s' % wallet_address).json()
        coinValue =requests.get('https://xchscan.com/api/chia-price').json()
        # Message Construction
        MSG_COINS = "%.2f XCH" % coins['xch']
        MSG_VALUE = "$%.2f USD" % float((coinValue['usd'] * coins['xch']))
        CHIA_PRICE = "$%.2f USD" % float(coinValue['usd'])
    except requests.exceptions.RequestException as e:
        continue
    except:
        continue
    
    # Constants
    WINDOW_SIZE = 360
    BAR_WIDTH = WINDOW_SIZE
    graph_valueS_LEFT = BAR_WIDTH + 5
    GRAPH_SIZE = (WINDOW_SIZE,100)
    PLOT_DATA_SIZE = (WINDOW_SIZE,100)
    DISK_DATA_SIZE = (WINDOW_SIZE,100)
    FONT = 'Times 48 bold ';

    if window == None: 
            
            # Window & Graph Setup
            graph_coins = sg.Graph(GRAPH_SIZE, (0,0), PLOT_DATA_SIZE, key='GRAPH-COINS')
            graph_value = sg.Graph(GRAPH_SIZE, (0,0), DISK_DATA_SIZE, key='GRAPH-VALUE')
            layout = [[graph_coins],[graph_value]]    
            window = sg.Window('Current Chia Price: %s' % CHIA_PRICE, layout, finalize=True)
                   
    else:
            # Delete Coins Graph Data
            graph_coins.delete_figure(coins_rect)
            graph_coins.delete_figure(coins_text)
            
             # Delete Value Graph Data
            graph_value.delete_figure(value_rect)
            graph_value.delete_figure(value_text)
    # (Re)Create Coins Graph
    coins_rect = graph_coins.DrawRectangle(top_left=(0, 100), bottom_right=(BAR_WIDTH, 0), fill_color='#009933')
    coins_text = graph_coins.DrawText(font=FONT, text=MSG_COINS, location=(BAR_WIDTH / 2, 100/2))

    # (Re)Create Value Graph
    value_rect = graph_value.DrawRectangle(top_left=(0, 100), bottom_right=(BAR_WIDTH, 0), fill_color='#ff8000')
    value_text = graph_value.DrawText(font=FONT,text=MSG_VALUE, location=(BAR_WIDTH / 2, 100/2))

    while True:
        event, values = window.Read(20000)
        break
    