"""
Time series analysis of the stocks to understand how good the stock is.
* Is it always increasing with minor fluctuations
* Is it always increasing with major fluctuations
* Is it mostly swinging with minor fluctuations
* Is it mostly swinging with major fluctuations
* Is it gradually decreasing with minor/major fluctuations

For such analysis, tsfel module is used.

Procedure:
  Load past 5 years data
  partition_steps = 1
  while partition_steps < 5:
    find [trend, seasonality, residue] from 'partition_steps' of data
    store [trend, seasonality, residue] into an array
    repeat until all the partitions are processed


"""
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime

# get stock data
def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Resampling to weekly data
    weekly_df = pd.DataFrame()
    weekly_df['Open'] = stock_data['Open'].resample('W').first()
    weekly_df['High'] = stock_data['High'].resample('W').max()
    weekly_df['Low'] = stock_data['Low'].resample('W').min()
    weekly_df['Close'] = stock_data['Close'].resample('W').last()
    weekly_df['Volume'] = stock_data['Volume'].resample('W').sum()
    weekly_df['Adj Close'] = stock_data['Adj Close'].resample('W').sum()

    # Display the new weekly data
    print(weekly_df)

    return stock_data, weekly_df


end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365*8)


sbin_data, weekly_data = get_stock_data("BEL.NS", start_date, end_date)

import tsfel
from statsmodels.tsa.seasonal import seasonal_decompose

series = sbin_data['Close']
decompose_result_add = seasonal_decompose(weekly_data['Close'], model='additive')
decompose_result_add.plot()
plt.show()

decompose_result_mul = seasonal_decompose(weekly_data['Close'], model='multiplicative')
decompose_result_mul.plot()
plt.show()

print(decompose_result_add.trend)
print(decompose_result_add.seasonal)
print(decompose_result_add.resid)
print(decompose_result_add.observed)



