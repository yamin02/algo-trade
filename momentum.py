## All this codes taken from chatgpt

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# Function to calculate momentum
def calculate_momentum(prices, lookback_period):
    momentum = (prices - prices.shift(lookback_period)) / prices.shift(lookback_period)
    return momentum

# Function to implement momentum trading strategy
def momentum_trading(ticker, start_date, end_date, lookback_period, buy_threshold, sell_threshold):
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date)
    print(data)
    
    # Calculate momentum
    data['Momentum'] = calculate_momentum(data['Adj Close'], lookback_period)
    
    # Initialize positions
    data['Position'] = 0
    
    # Buy signal: momentum > buy_threshold
    data.loc[ data['Momentum'] > buy_threshold, 'Position'] = 1
    
    # Sell signal: momentum < sell_threshold
    data.loc[ data['Momentum'] < sell_threshold, 'Position'] = -1
    
    # Calculate daily returns
    data['Returns'] = data['Adj Close'].pct_change()
    
    # Calculate strategy returns
    data['Strategy Returns'] = data['Position'].shift(1) * data['Returns']
    
    # Calculate cumulative returns
    data['Cumulative Returns'] = (data['Strategy Returns'] + 1).cumprod()
    
    return data

# Example usage
if __name__ == "__main__":
    ticker = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2022-01-01'
    lookback_period = 50  #Number of trading days used to calculate momentum
    buy_threshold = 0.05  # Buy if momentum > 5%
    sell_threshold = -0.05  # Sell if momentum < -5%
    
    strategy_data = momentum_trading(ticker, start_date, end_date, lookback_period, buy_threshold, sell_threshold)
    
    # Plot cumulative returns
    plt.figure(figsize=(10, 6))
    strategy_data['Cumulative Returns'].plot(title='Momentum Trading Strategy')
    plt.savefig('momentum_trading_plot.jpg', format='jpg')
    