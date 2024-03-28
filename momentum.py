## All this codes taken from chatgpt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from readcsv import parsedata

stockdata = parsedata('2018','GP' ,'2018-01-01', '2018-12-31')

# Function to calculate momentum
def calculate_momentum(prices, lookback_period):
    momentum = (prices - prices.shift(lookback_period)) / prices.shift(lookback_period)
    # price of stock 50 days before minus from price today
    return momentum

# Function to implement momentum trading strategy
def momentum_trading(ticker, start_date, end_date, lookback_period, buy_threshold, sell_threshold):
    # Download historical data
    data = parsedata('2018', ticker ,start_date , end_date)
    print(data)
    
    # Calculate momentum
    data['Momentum'] = calculate_momentum(data['close'], lookback_period)
    
    # Initialize positions
    data['Position'] = 0
    
    # Buy signal: momentum > buy_threshold
    data.loc[ data['Momentum'] > buy_threshold, 'Position'] = 1
    
    # Sell signal: momentum < sell_threshold
    data.loc[ data['Momentum'] < sell_threshold, 'Position'] = -1
    
    # Calculate daily returns : .pct_change() method is used to calculate 
    # the percentage change between the current and the previous element in a Series or DataFrame
    data['Returns'] = data['close'].pct_change()
    
    # strategy return :  multiplying yesterday's position with today's returns.
    data['Strategy Returns'] = data['Position'].shift(1) * data['Returns']
    
    # Calculate cumulative returns
    data['Cumulative Returns'] = (data['Strategy Returns'] + 1).cumprod()
    return data

# Example usage
if __name__ == "__main__":
    ticker = 'GP'
    start_date = '2018-01-01'
    end_date = '2018-12-01'
    lookback_period = 50  #Number of trading days used to calculate momentum
    buy_threshold = 0.05  # Buy if momentum > 5%
    sell_threshold = -0.05  # Sell if momentum < -5%
    
    strategy_data = momentum_trading(ticker, start_date, end_date, lookback_period, buy_threshold, sell_threshold)
    
    # Plot cumulative returns
    plt.figure(figsize=(10, 6))
    strategy_data['Cumulative Returns'].plot(title='Momentum Trading Strategy')
    plt.savefig('momentum_trading_plot.jpg', format='jpg')
    