import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulated historical price data for two stocks
stock1_prices = np.random.normal(loc=100, scale=10, size=100)
stock2_prices = stock1_prices + np.random.normal(loc=0, scale=5, size=100)

# Calculate the spread between the two stocks
spread = stock1_prices - stock2_prices

# Define parameters
lookback_period = 30  # Number of days to look back
entry_threshold = 2.0  # Entry threshold for spread deviation
exit_threshold = 0.5  # Exit threshold for spread deviation
position_size = 1  # Number of shares to trade

# Initialize positions
stock1_position = 0
stock2_position = 0
positions = []

# Iterate over historical data
for i in range(lookback_period, len(spread)):
    spread_mean = np.mean(spread[i - lookback_period:i])
    spread_std = np.std(spread[i - lookback_period:i])
    z_score = (spread[i] - spread_mean) / spread_std
    
    # Check for entry signal
    if z_score > entry_threshold:
        # Short stock1 and long stock2
        stock1_position -= position_size
        stock2_position += position_size
    elif z_score < -entry_threshold:
        # Long stock1 and short stock2
        stock1_position += position_size
        stock2_position -= position_size
    
    # Check for exit signal
    elif abs(z_score) < exit_threshold:
        # Close positions
        stock1_position = 0
        stock2_position = 0
    
    positions.append((stock1_position, stock2_position))

# Visualize positions
positions_df = pd.DataFrame(positions, columns=['Stock1', 'Stock2'])
plt.figure(figsize=(10, 6))
plt.plot(positions_df['Stock1'], label='Stock1 Position')
plt.plot(positions_df['Stock2'], label='Stock2 Position')
plt.title('Pairs Trading Positions')
plt.xlabel('Time')
plt.ylabel('Position')
plt.legend()
plt.show()
