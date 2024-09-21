# This code is taken from https://eodhd.com/financial-academy/backtesting-strategies-examples/backtesting-a-killer-mean-reversion-trading-strategy-with-python

import pandas as pd
import pandas_ta as ta
from datetime import datetime
from termcolor import colored as cl
import math 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from getdata import parsedata,parsedata2

# Fetching historical stock data
stock_symbol = "ADNTEL"
start_date = "2023-01-01"
end_date = "2024-04-22"
stock_data = parsedata2(stock_symbol, start_date , end_date)
stock_data['close'] = stock_data['close'].astype(float)
stock_data["volume"] = stock_data["volume"].astype(float)
print('Data parsed')


# RSI & SMA CALCULATION

stock_data['sma200'] = ta.sma(stock_data.close, length = 24)
stock_data['rsi10'] = ta.rsi(stock_data.close, length = 7)
ta.e
stock_data = stock_data.dropna().reset_index()
# .drop('index', axis = 1)

stock_data.tail()

print(stock_data)

# aapl_df['rsi10'][i] < 30 and aapl_df['close'][i] > aapl_df['sma200'][i]

# CREATING & BACKTESTING THE STRATEGY
def implement_strategy(aapl_df, investment):
    in_position = False
    equity = investment
    for i in range(3, len(aapl_df)):fd
        if aapl_df['close'][i] > aapl_df['sma200'][i] and in_position == False:
            no_of_shares = math.floor(equity/aapl_df.close[i])
            equity -= (no_of_shares * aapl_df.close[i])
            in_position = True
            print(cl('BUY: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at ${aapl_df.close[i]} on {aapl_df.date[i]}')
        
        elif aapl_df['close'][i] < aapl_df['sma200'][i] and in_position == True:
            equity += (no_of_shares * aapl_df.close[i])
            in_position = False
            print(cl('SELL: ', color = 'red', attrs = ['bold']), f'{no_of_shares} Shares are bought at ${aapl_df.close[i]} on {aapl_df.date[i]}')
    if in_position == True:
        equity += (no_of_shares * aapl_df.close[i])
        print(cl(f'\nClosing position at {aapl_df.close[i]} on {aapl_df.date[i]}', attrs = ['bold']))
        in_position = False

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    print('')
    print(cl(f'EARNING: ${earning} ; ROI: {roi}%', attrs = ['bold']))
    

implement_strategy(stock_data, 100000)

