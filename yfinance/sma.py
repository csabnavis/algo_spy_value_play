#### Strategy: Buy if sma 20 > sma50; sell otherwise
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

# import data
def import_data(stocks, start, end):
    return yf.download(stocks, start, end)

stocks = ['AAPL']
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=3650) #10 years

data = import_data(stocks, startDate, endDate)
data = data[['Adj Close']]
data.rename(columns={'Adj Close': 'Price'}, inplace=True) # Rename column
data['SMA_20'] = data['Price'].rolling(20).mean()
data['SMA_50'] = data['Price'].rolling(50).mean()

# Create signal column based on SMA crossover
data['Signal'] = 0 # Initialize signal column with zeros
data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1 # Buy signal
data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1 # Sell signal


# Plot price data and SMAs along with buy and sell signals
plt.figure(figsize=(15,10)) # Set figure size
plt.plot(data['Price'], label='Price') # Plot price
plt.plot(data['SMA_20'], label='SMA_20') # Plot SMA_20
plt.plot(data['SMA_50'], label='SMA_50') # Plot SMA_50
plt.scatter(data.index, data['Price'], c=data['Signal'], cmap='coolwarm', 
            edgecolors='black', label='Signal') # Plot buy and sell signals
plt.title('Moving Average Crossover Strategy') # Set title
plt.xlabel('Date') # Set x-axis label
plt.ylabel('Price') # Set y-axis label
plt.legend() # Show legend
plt.show() # Show plot

# Calculate returns and cumulative returns of the strategy
data['Return'] = data['Price'].pct_change() # Calculate daily return
data['Strategy_Return'] = data['Return'] * data['Signal'].shift(1) # Calculate strategy return
data['Cumulative_Return'] = (1 + data['Return']).cumprod() # Calculate cumulative return of buy-and-hold strategy
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod() # Calculate cumulative return of MA crossover strategy

# Plot cumulative returns of the strategy and compare with buy-and-hold strategy
plt.figure(figsize=(15,10)) # Set figure size
plt.plot(data['Cumulative_Return'], label='Buy and Hold') # Plot cumulative return of buy-and-hold strategy
plt.plot(data['Cumulative_Strategy_Return'], label='MA Crossover') # Plot cumulative return of MA crossover strategy
plt.title('Cumulative Returns of Moving Average Crossover Strategy') # Set title
plt.xlabel('Date') # Set x-axis label
plt.ylabel('Cumulative Return') # Set y-axis label
plt.legend() # Show legend
plt.show() # Show plot