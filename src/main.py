import time

import numpy as np
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


def get_stock_list(stock_info_excel):
    # read by default 1st sheet of an excel file
    stock_info_df = pd.read_excel(stock_info_excel)
    return stock_info_df["STOCK_NAME"].tolist()


if __name__ == '__main__':
    stock_info_excel = r"D:\git\Stocks\src\data\stocks.xlsx"
    stock_list = get_stock_list(stock_info_excel)
    stock_buy_likelihood = {}
    BOLINGER_LIKELIHOOD = []
    RSI_LIKELIHOOD = []
    RSI_LEVEL = []
    STOCKS = []

    count = 0
    for stock in stock_list:
        #stock = "ASKAUTOLTD"
        if stock in ["ADANIPOWER"]:
            continue
        fetch_obj = Fetch()
        try:
            fetch_obj.set_stock_symbol(stock)
        except:
            print(f"Stock not found: {stock}")
            continue
        else:
            print(f"Procssing {stock}")

        fetch_obj.set_timeframe(weeks=60)

        # fetch data for the stock. If invalid name, continue
        if fetch_obj.fetch_data() is None:
            print(f"{stock}: Invalid stock name for query!")
            continue

        daily_data = fetch_obj.get_daily_data()

        count+= 1
        time.sleep(2)

        resample_obj = Resample()
        resample_obj.set_stock_df(daily_data)
        resample_obj.resample_weekly()
        weekly_data = resample_obj.get_weekly_data()

        daily_analysis_obj = Analyse()
        daily_analysis_obj.set_data(daily_data)
        bolinger_band_buy_likelihood, rsi_buy_likelihood, rsi_buy_level = daily_analysis_obj.analyse_indicators()

        stock_buy_likelihood[stock] = {"BOLINGER_LIKELIHOOD": bolinger_band_buy_likelihood,
                                       "RSI_LIKELIHOOD": rsi_buy_likelihood,
                                       "RSI_LEVEL": rsi_buy_level}
        BOLINGER_LIKELIHOOD.append(bolinger_band_buy_likelihood)
        RSI_LIKELIHOOD.append(rsi_buy_likelihood)
        RSI_LEVEL.append(rsi_buy_level)
        STOCKS.append(stock)

        print(stock_buy_likelihood[stock])
        if count > 600:
            break

    df = pd.DataFrame({'BOLINGER_LIKELIHOOD': BOLINGER_LIKELIHOOD,
                       'RSI_LIKELIHOOD': RSI_LIKELIHOOD,
                       'RSI_LEVEL': RSI_LEVEL,
                       'STOCKS': STOCKS})

    # Set the index
    df.index = np.arange(len(STOCKS))


    print(df)
    # saving the dataframe
    df.to_csv('stock_analysis.csv')

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