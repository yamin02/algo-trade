import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from getdata import parsedata,parsedata2


# Fetching historical stock data
stock_symbol = "ROBI"
start_date = "2023-01-01"
end_date = "2024-04-22"
stock_data = parsedata2(stock_symbol, start_date , end_date)
stock_data['close'] = stock_data["close"].astype(float)
print('Data parsed')

# Calculating daily returns
stock_data['Daily_Return'] = stock_data['close'].pct_change()

# Calculating volatility (multiply by sqroot(no. of days))
volatility = stock_data['Daily_Return'].std() * np.sqrt(len(stock_data['close']))

# Plotting the volatility
plt.figure(figsize=(10, 6))
stock_data['Daily_Return'].plot()
plt.title(f'Volatility of {stock_symbol}')
plt.ylabel('Daily Returns')
plt.xlabel('Date')
plt.savefig(f'./plots/volatillity_{stock_symbol}.jpg', format='jpg' , dpi=720)
print("DONE WITH plot")