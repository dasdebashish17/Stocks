import yfinance as yf
import datetime
import pandas as pd
import ta  # This library provides technical indicators
import numpy as np


def compute_support_levels(data, cumulative_level):
    """
    Compute the support levels for the data
    :param data:
    :return:
    """
    # For computing histogram, we need to convert data from float to integer
    scaled_data = np.int32(data)
    # compute histogram
    hist, bin_edges = np.histogram(scaled_data, bins=20)
    hist_normalized = hist / sum(hist)
    # compute cumulative values
    cdf = np.cumsum(hist_normalized)
    # find the level which corresponds to 0.12 in cdf
    for idx in range(len(cdf)):
        if cdf[idx] > cumulative_level:
            y_diff = cdf[idx] - cdf[idx - 1]
            x_diff = bin_edges[idx + 1] - bin_edges[idx]
            x_interpolated = bin_edges[idx] + ((cumulative_level - cdf[idx - 1]) * x_diff / y_diff)
            break

    return x_interpolated



def get_stock_list(stock_info_excel):
    # read by default 1st sheet of an excel file
    stock_info_df = pd.read_excel(stock_info_excel)
    stock_list = stock_info_df["STOCK_NAME"].tolist()
    stock_list = [f"{stock}.NS" for stock in stock_list]
    return stock_list


# Get today's date and one year ago date
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

# List of NSE stock symbols (remember to append '.NS' for NSE stocks)
stock_info_excel = r"D:\git\Stocks\src\data\stocks.xlsx"
symbols = get_stock_list(stock_info_excel)

def fetch_stock_data_and_indicators(symbol):
    """
    Function to fetch stock data and calculate indicators for a single stock symbol
    """
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
    except:
        return None


    # Calculate indicators if data is available
    if not stock_data.empty:
        # Moving Average (50 days)
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()

        # Relative Strength Index (RSI)
        stock_data['RSI'] = ta.momentum.RSIIndicator(stock_data['Close']).rsi()

        # Bollinger Bands (20-day moving average and standard deviation)
        bollinger = ta.volatility.BollingerBands(stock_data['Close'])
        stock_data['Bollinger_High'] = bollinger.bollinger_hband()
        stock_data['Bollinger_Low'] = bollinger.bollinger_lband()

    return stock_data


# Dictionary to store stock data and indicators for each stock
stock_data_dict = {}

# Sequentially fetch stock data and calculate indicators for each stock
invalid_symbols = []
valid_symbols = []
close_prices = []
rsis = []
ma50s = []
bollinger_highs = []
bollinger_lows = []
rsi_buy_levels = []
rsi_sell_levels = []

COUNT = 0
for symbol in symbols:
    stock_data = fetch_stock_data_and_indicators(symbol)
    if stock_data is None or stock_data.empty:
        print(f"{symbol} is not available!")
        invalid_symbols.append(symbol)
        continue
    stock_data_dict[symbol] = stock_data
    #print(f"Stock data with indicators for {symbol}:")
    print(stock_data[['Close', 'MA50', 'RSI', 'Bollinger_High', 'Bollinger_Low']].tail(), "\n")

    print(symbol)
    rsi_data = [x for x in stock_data['RSI'].tolist() if not np.isnan(x)]
    rsi_buy_level = compute_support_levels(rsi_data, 0.12)
    rsi_sell_level = compute_support_levels(rsi_data, 0.86)

    valid_symbols.append(symbol)
    close_prices.append(stock_data['Close'].iloc[-1])
    rsis.append(stock_data['RSI'].iloc[-1])
    ma50s.append(stock_data['MA50'].iloc[-1])
    bollinger_highs.append(stock_data['Bollinger_High'].iloc[-1])
    bollinger_lows.append(stock_data['Bollinger_Low'].iloc[-1])
    rsi_buy_levels.append(rsi_buy_level)
    rsi_sell_levels.append(rsi_sell_level)
    COUNT += 1
    if COUNT > 1000:
        break




df = pd.DataFrame({'STOCKS': valid_symbols,
                   'CLOSE': close_prices,
                   'RSI':rsis,
                   'MA50': ma50s,
                   'BOLLINGER_HIGH': bollinger_highs,
                   'BOLLINGER_LOW': bollinger_lows,
                   'RSI_BUY_LEVEL': rsi_buy_levels,
                   'RSI_SELL_LEVEL': rsi_sell_levels
                   })

# Set the index
df.index = np.arange(len(valid_symbols))
df['RSI_BUY_LIKELIHOOD'] = (df['RSI_BUY_LEVEL'] - df['RSI']) / df['RSI_BUY_LEVEL']
df['BOLLINGER_BUY_LIKELIHOOD'] = (df['BOLLINGER_LOW'] - df['CLOSE']) / df['BOLLINGER_LOW']
print(df)
# saving the dataframe
df.to_csv('stock_analysis.csv')


import plotly.express as px

fig = px.scatter(df, x="RSI_BUY_LIKELIHOOD", y="BOLLINGER_BUY_LIKELIHOOD",
                 hover_data=["STOCKS", "RSI_BUY_LEVEL", "RSI_SELL_LEVEL"])

fig.show()