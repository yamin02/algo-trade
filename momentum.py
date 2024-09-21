## THIS IS FOR MOMENTUM TRADING

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from getdata import parsedata2

# stockdata = parsedata('2018','GP' ,'2018-01-01', '2018-12-31')

# Function to calculate momentum
def calculate_momentum(prices, lookback_period):
    momentum = ((prices) - (prices.shift(lookback_period)) ) / prices.shift(lookback_period)
    # price of stock 50 days before minus from price today
    return momentum

# Function to implement momentum trading strategy
def momentum_trading(ticker, start_date, end_date, lookback_period, buy_threshold, sell_threshold):
    # Download historical data
    data = parsedata2(ticker ,start_date , end_date)
    print('Data parsed')
    
    # Calculate momentum
    data['Momentum'] = calculate_momentum(data['close'].astype(float) , lookback_period)
    print('done momentum')
    # Initialize positions
    data['Position'] = 0
    
    # Buy signal: momentum > buy_threshold
    data.loc[ data['Momentum'] > buy_threshold, 'Position'] = 1
    
    # Short Selling signal: momentum < sell_threshold
    # data.loc[ data['Momentum'] < sell_threshold, 'Position'] = -1
    
    # Calculate daily returns : .pct_change(2) method is used to calculate two day ago price
    # the percentage change between the current and the previous element in a Series or DataFrame
    data['Returns'] = (data['close'].astype(float)).pct_change(2) 
    
    # strategy return (sell the stock the next day of buying ) :  multiplying two day ago's (because settlement in one day) position with today's returns.
    data['Strategy Returns'] = data['Position'].shift(2) * data['Returns'] 
    
    # Calculate cumulative returns
    data['Cumulative Returns'] = (data['Strategy Returns'] + 1).cumprod()
    print(f"Max Cumulative Return {ticker} = {data['Cumulative Returns'].max()}")
    return data


fig, ax = plt.subplots()

# Example usage
if __name__ == "__main__":
    tickers = [ 'GENEXIL' , 'ADNTEL' , 'AIL' , 'DGIC' , 'INTRACO']
    start_date = '2023-01-01'
    end_date = '2024-03-24'
    lookback_period = 7  #Number of trading days used to calculate momentum
    buy_threshold = 0.05  # Buy if momentum > 5%
    sell_threshold = -0.05  # Sell if momentum < -5%
    
    for ticker in tickers:
        strategy_data = momentum_trading(ticker, start_date, end_date, lookback_period, buy_threshold, sell_threshold)
        # Plot cumulative returns
        # plt.figure(figsize=(10, 6))
        strategy_data['Cumulative Returns'].plot(ax=ax , label =f'{ticker}' )

plt.legend()
plt.title(f'Cumulative return for Momentum trading with look back {lookback_period} days')
plt.savefig(f'./plots/mom_trade2.jpg', format='jpg' , dpi=720)
