import pandas as pd
import sys

# Insert the path of modules folder
sys.path.insert(0, "analyse")
sys.path.append("analyse\\indicator")
sys.path.append("data")
sys.path.append("fetch")

from fetch import Fetch
from resample import Resample
from analyse import Analyse

# This is the main code which accesses various source codes to perform various operations
class Stocks:
    pass


if __name__ == '__main__':
    fetch_obj = Fetch()
    fetch_obj.set_stock_symbol("IRCON")
    fetch_obj.set_timeframe()
    fetch_obj.fetch_data()
    fetch_obj.plot_data()
    daily_data = fetch_obj.get_daily_data()

    resample_obj = Resample()
    resample_obj.set_stock_df(daily_data)
    resample_obj.resample_weekly()
    weekly_data = resample_obj.get_weekly_data()

    daily_analysis_obj = Analyse()
    daily_analysis_obj.set_data(daily_data)
    buy_indicator = daily_analysis_obj.analyse_indicators()






"""
# Compute the high, low, and closing prices for the stock
high = prices["High"]
low = prices["Low"]
close = prices["Close"]

# Find the rolling maximum and minimum for the high and low prices
rolling_max = high.rolling(20).max().mean()
rolling_min = low.rolling(20).min().mean()

# Identify the support levels as the rolling minimum
support = rolling_min

# Identify the resistance levels as the rolling maximum
resistance = rolling_max

# Print the support and resistance levels
print("Support levels:", support)
print("Resistance levels:", resistance)
"""