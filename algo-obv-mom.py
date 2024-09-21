import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from getdata import parsedata,parsedata2

# Fetching historical stock data
stock_symbol = "ITC"
start_date = "2023-01-01"
end_date = "2024-04-22"
stock_data = parsedata2(stock_symbol, start_date , end_date)
stock_data['close'] = stock_data['close'].astype(float)
stock_data["volume"] = stock_data["volume"].astype(float)
print('Data parsed')

# Calculating the On-Balance Volume (OBV)
obv = [0]
for i in range(1, len(stock_data)):
    if stock_data['close'][i] > stock_data['close'][i-1]:
        obv.append(obv[-1] + stock_data['volume'][i])
    elif stock_data['close'][i] < stock_data['close'][i-1]:
        obv.append(obv[-1] - stock_data['volume'][i])
    else:
        obv.append(obv[-1])

stock_data['OBV'] = obv

# Adding Momentum to DataFrame
def calculate_momentum(data, period=7):
	return data['close'].diff(periods=period)
stock_data['Momentum'] = calculate_momentum(stock_data)



def trading_strategy(data):
    buy_signals = []
    sell_signals = []
    
    for i in range(len(data)):
        # Buy if momentum is positive and OBV is increasing
        if data['Momentum'][i] > 0 and data['OBV'][i] > data['OBV'][i-1]:
            buy_signals.append(data['close'][i])
            sell_signals.append(np.nan)
        # Sell if momentum is negative
        elif data['Momentum'][i] < 0:
            sell_signals.append(data['close'][i])
            buy_signals.append(np.nan)
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    return buy_signals, sell_signals

stock_data['Buy_Signals'], stock_data['Sell_Signals'] = trading_strategy(stock_data)

#visualize data
plt.figure(figsize=(12,6))
plt.plot(stock_data['close'], label='Close Price', alpha=0.5)
plt.scatter(stock_data.index, stock_data['Buy_Signals'], label='Buy Signal', marker='^', color='green')
plt.scatter(stock_data.index, stock_data['Sell_Signals'], label='Sell Signal', marker='v', color='red')
plt.title(f'Momentum Trading Signals for {stock_symbol}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
# plt.show()
plt.savefig(f'./plots/obv_mom_{stock_symbol}.jpg', format='jpg' , dpi=720)
print("DONE WITH plot")