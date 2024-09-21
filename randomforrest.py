from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
from getdata import parsedata2

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
def calculate_momentum(data, period=1):
	return data['close'].diff(periods=period)
stock_data['Momentum'] = calculate_momentum(stock_data)

#remove NaN from data frame
stock_data = stock_data.dropna()

#Get the trading strategy
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

# Features can include 'Momentum', 'OBV', and other technical indicators
# Target is whether to buy (1), hold (0), or sell (-1)

X = stock_data[['Momentum', 'OBV']]

# Dont know what to give me , Need to learn more 
y = stock_data["Buy_Signals"]
print(y)
# You can define target based on trading strategy

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Training the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Testing the model
predictions = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, predictions)}")