import yfinance as yf
import datetime
import pandas as pd
import ta  # This library provides technical indicators
import numpy as np
import os
from typing import Union




def get_stock_list(stock_info_excel) -> list:
    """
    Get the stocks list from the specified excel file
    :param stock_info_excel: file containing stock info
    :return: list of stock symbols (in sorted order) which can be queried using yfinance package
    """
    if not os.path.isfile(stock_info_excel):
        print(f"FILE NOT FOUND: {stock_info_excel}")
        return None

    # read by default 1st sheet of an excel file
    stock_info_df = pd.read_excel(stock_info_excel)
    stock_list = stock_info_df["STOCK_NAME"].tolist()
    stock_list = sorted(list(set([f"{stock}.NS" for stock in stock_list])))
    return sorted(stock_list)



def compute_support_levels(data:np.ndarray, cumulative_level:float) -> float:
    """
    Compute the support levels for the specified data which corresponds to the specified cumulative level
    :param data: Data (RSI, stock price etc) for which support level needs to be computed
    :param cumulative_level: CDF level which corresponds to the support
    :return: support level
    """
    # For computing histogram, we need to convert data from float to integer
    scaled_data = np.int32(data)
    # compute histogram
    hist, bin_edges = np.histogram(scaled_data, bins=20)
    try:
        hist_normalized = hist / sum(hist)
    except:
        print(f"Inspect hist:{hist}")

    # compute cumulative values
    cdf = np.cumsum(hist_normalized)
    # find the level which corresponds to 0.12 in cdf
    for idx in range(len(cdf)):
        if cdf[idx] > cumulative_level:
            y_diff = cdf[idx] - cdf[idx - 1]
            x_diff = bin_edges[idx + 1] - bin_edges[idx]
            support_level = bin_edges[idx] + ((cumulative_level - cdf[idx - 1]) * x_diff / y_diff)
            break

    return support_level



def update_indicators(stock_df:pd.DataFrame):
    """
    Compute the stock indicators using the data specified
    :param data: stock data usually the closing values
    :return:
    """
    # use closing price to compute the indicators
    data = stock_df['Close']

    # Moving Average (50 days)
    stock_df['MA50'] = data.rolling(window=50).mean()

    # Relative Strength Index (RSI)
    stock_df['RSI'] = ta.momentum.RSIIndicator(data).rsi()

    # Bollinger Bands (20-day moving average and standard deviation)
    bollinger = ta.volatility.BollingerBands(data)
    stock_df['Bollinger_High'] = bollinger.bollinger_hband()
    stock_df['Bollinger_Low'] = bollinger.bollinger_lband()



def compute_weekly_data(daily_data:pd.DataFrame) -> pd.DataFrame:
    """
    From daily data, compute the weekly data
    :param daily_data: daily stock data
    :return: weekly stock data
    """
    # Resampling to weekly data
    weekly_data = pd.DataFrame()
    weekly_data['Open'] = daily_data['Open'].resample('W').first()
    weekly_data['High'] = daily_data['High'].resample('W').max()
    weekly_data['Low'] = daily_data['Low'].resample('W').min()
    weekly_data['Close'] = daily_data['Close'].resample('W').last()
    weekly_data['Volume'] = daily_data['Volume'].resample('W').sum()
    weekly_data['Adj Close'] = daily_data['Adj Close'].resample('W').sum()

    return weekly_data



def fetch_daily_stock_data(stock_symbol:str) -> pd.DataFrame:
    """
    Fetch daily stock data
    :param symbol:
    :return:
    """
    try:
        stock_data_daily = yf.download(stock_symbol, start=start_date, end=end_date)
    except:
        stock_data_daily =  None

    return stock_data_daily



def get_marketcap(stock_symbol:str) -> float:
    """
    Get the market cap of a stock
    :param stock_symbol:
    :return:
    """
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info

    # Check if market cap information is available
    market_cap = stock_info.get("marketCap")
    return market_cap



def fetch_stock_data_and_indicators(symbol) -> Union[pd.DataFrame, pd.DataFrame]:
    """
    Function to fetch stock data and calculate indicators for a single stock symbol
    :param symbol: stock symbol
    :return:
    """
    # fetch daily stock data
    stock_data_daily = fetch_daily_stock_data(symbol)

    if stock_data_daily is not None:
        # Resampling to weekly data
        stock_data_weekly = compute_weekly_data(stock_data_daily)

        # Calculate indicators if daily data is available
        if not stock_data_daily.empty:
            # update the indicators information
            update_indicators(stock_data_daily)

        # Calculate indicators if weekly data is available
        if not stock_data_weekly.empty:
            # update the indicators information
            update_indicators(stock_data_weekly)

        return stock_data_daily, stock_data_weekly

    else:
        return None, None




def update_latest_parameters(stock_symbol:str, stock_data:pd.DataFrame, stocks_summary_dict:dict):
    """
    Update the latest parameters for the stock
    :param stock_data: daily stock data
    :return:
    """
    # get the valid RSI values (initial few entries can be None which needs to be eliminated)
    rsi_data = [x for x in stock_data['RSI'].tolist() if not np.isnan(x)]
    # compute the buy and sell levels for RSI
    rsi_buy_level = compute_support_levels(np.array(rsi_data), 0.12)
    rsi_sell_level = compute_support_levels(np.array(rsi_data), 0.86)

    stocks_summary_dict['STOCKS'].append(stock_symbol)
    stocks_summary_dict['CLOSE'].append(stock_data['Close'].iloc[-1])
    stocks_summary_dict['RSI'].append(stock_data['RSI'].iloc[-1])
    stocks_summary_dict['MA50'].append(stock_data['MA50'].iloc[-1])
    stocks_summary_dict['BOLLINGER_HIGH'].append(stock_data['Bollinger_High'].iloc[-1])
    stocks_summary_dict['BOLLINGER_LOW'].append(stock_data['Bollinger_Low'].iloc[-1])
    stocks_summary_dict['RSI_BUY_LEVEL'].append(rsi_buy_level)
    stocks_summary_dict['RSI_SELL_LEVEL'].append(rsi_sell_level)



def update_buy_likelihood(summary_df: pd.DataFrame):
    """
    Update the buy likelihood based on the RSI and Bolinger band levels
    :param summary_df:
    :return:
    """
    summary_df['RSI_BUY_LIKELIHOOD'] = (summary_df['RSI_BUY_LEVEL'] - summary_df['RSI']) / summary_df['RSI_BUY_LEVEL']
    summary_df['BOLLINGER_BUY_LIKELIHOOD'] = (summary_df['BOLLINGER_LOW'] - summary_df['CLOSE']) / summary_df['BOLLINGER_LOW']



# Get today's date and one year ago date
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365*4)

# List of NSE stock symbols (remember to append '.NS' for NSE stocks)
stock_info_excel = r"D:\git\Stocks\src\data\stocks.xlsx"
symbols = get_stock_list(stock_info_excel)



# Sequentially fetch stock data and calculate indicators for each stock
invalid_symbols = []

summary_template = {'STOCKS': [],
                    'CLOSE': [],
                    'RSI':[],
                    'MA50': [],
                    'BOLLINGER_HIGH': [],
                    'BOLLINGER_LOW': [],
                    'RSI_BUY_LEVEL': [],
                    'RSI_SELL_LEVEL': [] }

daily_summary_dict = {'STOCKS': [],
                    'CLOSE': [],
                    'RSI':[],
                    'MA50': [],
                    'BOLLINGER_HIGH': [],
                    'BOLLINGER_LOW': [],
                    'RSI_BUY_LEVEL': [],
                    'RSI_SELL_LEVEL': [] }

weekly_summary_dict = {'STOCKS': [],
                    'CLOSE': [],
                    'RSI':[],
                    'MA50': [],
                    'BOLLINGER_HIGH': [],
                    'BOLLINGER_LOW': [],
                    'RSI_BUY_LEVEL': [],
                    'RSI_SELL_LEVEL': [] }


COUNT = 0
for symbol in symbols:
    if 'AARTIIND' in symbol:
        pass

    stock_data_daily, stock_data_weekly = fetch_stock_data_and_indicators(symbol)
    if stock_data_daily is None or stock_data_daily.empty:
        invalid_symbols.append(symbol)
        continue

    print(f"******* {symbol} ******")
    print(stock_data_daily.size)
    print(stock_data_daily[['Close', 'MA50', 'RSI', 'Bollinger_High', 'Bollinger_Low']].tail(), "\n")

    update_latest_parameters(symbol, stock_data_daily, daily_summary_dict)
    update_latest_parameters(symbol, stock_data_weekly, weekly_summary_dict)

    COUNT += 1
    if COUNT > 1000:
        break


daily_summary_df = pd.DataFrame(daily_summary_dict)
weekly_summary_df = pd.DataFrame(weekly_summary_dict)


# Set the index
#daily_summary_df.index = np.arange(len(valid_symbols))
update_buy_likelihood(daily_summary_df)
update_buy_likelihood(weekly_summary_df)

# saving the dataframe
daily_summary_df.to_csv('daily_stock_analysis.csv')
weekly_summary_df.to_csv('weekly_stock_analysis.csv')


import plotly.express as px

fig = px.scatter(daily_summary_df, x="RSI_BUY_LIKELIHOOD", y="BOLLINGER_BUY_LIKELIHOOD",
                 hover_data=["STOCKS", "RSI_BUY_LEVEL", "RSI_SELL_LEVEL", "CLOSE"], title="RSI vs BOLLINGER (DAILY)")

fig.show()

fig = px.scatter(weekly_summary_df, x="RSI_BUY_LIKELIHOOD", y="BOLLINGER_BUY_LIKELIHOOD",
                 hover_data=["STOCKS", "RSI_BUY_LEVEL", "RSI_SELL_LEVEL", "CLOSE"], title="RSI vs BOLLINGER (WEEKLY)")

fig.show()
