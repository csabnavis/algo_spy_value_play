import numpy as np
import pandas as pd
from scipy import stats
import pathlib
import yfinance as yf
from config import SPY_DATA_FOLDER

#read file from spy_data
files = pathlib.Path(SPY_DATA_FOLDER).glob('**/*.xlsx')
dataFile = next(files, None)
df = pd.read_excel(dataFile, skiprows=4)

# Instead of sending all at once, call yfinance in chunks and merge
# tickers = df['Ticker']

tickers = df['Ticker'].dropna()
tickerStr = ','.join(tickers)

tickerStr = tickerStr.replace('.','-')
tickerData = yf.Tickers(tickerStr)
print('Received ticker information.')


requiredColumns = ['Ticker', 'Price', 'Price-to-Earnings', 'Shares to Buy']
stock_data = pd.DataFrame(columns=requiredColumns)

for ticker in tickerStr.split(','):
    if ticker != '-':
        current_price = tickerData.tickers[ticker].history(period="1d")["Close"].iloc[0]

        try:
            trailing_pe = tickerData.tickers[ticker].info["trailingPE"]
        except KeyError:
            trailing_pe = 'N/A'

        stock_data = stock_data._append(
            pd.Series(
                [
                    tickerData.tickers[ticker].ticker,
                    current_price,
                    1,
                    'N/A'
                ],
                index= requiredColumns
            ),
            ignore_index = True
        )

print(stock_data)

    
