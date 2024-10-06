import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from matplotlib import pyplot as plt
from nsepython import *

import plotly.graph_objects as go

from stock_indicators import indicators, Quote # https://python.stockindicators.dev/indicators/#content



class Indicator:
    """
    Class to compute various indicators associated with a stock
    """
    def __init__(self):
        pass


    def set_params(self, date, open_price, high_price, low_price, close_price, volume):
        """
        Set the parameters to be used for indicator generation
        :param date:
        :param open_price:
        :param high_price:
        :param low_price:
        :param close_price:
        :param volume:
        :return:
        """
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume


    def update_quote_list(self):
        """
        Update the quote list
        :return:
        """
        datetime_list = []
        for date_str in self.date:
            year, month, date = re.findall("(\d+)-(\d+)-(\d+)", date_str)[0]
            datetime_list.append(datetime.datetime(int(year), int(month), int(date), 0, 0, 0))

        self.quotes_list = [ Quote(date, open, high, low, close, volume) for date, open, high, low, close, volume
                             in zip(datetime_list, self.open_price, self.high_price, self.low_price, self.close_price, self.volume)]


    def compute_support_levels(self, data):
        """
        Compute the support levels for the data
        :param data:
        :return:
        """
        # For computing histogram, we need to convert data from float to integer
        scaled_data = np.int32(data[data != None])
        # compute histogram
        hist, bin_edges = np.histogram(scaled_data, bins=20)
        hist_normalized = hist / sum(hist)
        # compute cumulative values
        cdf = np.cumsum(hist_normalized)
        # find the level which corresponds to 0.12 in cdf
        for idx in range(len(cdf)):
            if cdf[idx] > 0.10:
                y_diff = cdf[idx] - cdf[idx-1]
                x_diff = bin_edges[idx+1] - bin_edges[idx]
                x_interpolated = bin_edges[idx] + ((0.12 - cdf[idx-1]) * x_diff / y_diff)
                break

        return x_interpolated


    def compute_bolinger_band(self):
        """
        compute the bolinger band indicators
        :return:
        """
        self.bolinger_band_data = {}
        bolinger_band_results = indicators.get_bollinger_bands(self.quotes_list, 20, 2)
        self.bolinger_band_data["sma"] = [r.sma for r in bolinger_band_results]
        self.bolinger_band_data["lower_band"] = [r.lower_band for r in bolinger_band_results]
        self.bolinger_band_data["upper_band"] = [r.upper_band for r in bolinger_band_results]


    def compute_macd(self):
        """
        Compute the macd indicators
        :return:
        """
        macd_results = indicators.get_macd(self.quotes_list, 12, 26, 9)
        self.macd_data = [r.macd for r in macd_results]


    def compute_rsi(self):
        """
        Compute the RSI indicators
        :return:
        """
        rsi_results = indicators.get_rsi(self.quotes_list, 14)
        self.rsi_data = np.array([r.rsi for r in rsi_results])
        self.rsi_threshold = self.compute_support_levels(self.rsi_data)

        return





    def compute_support(self):
        """
        Compute the support limits
        :return:
        """
        pass


    def compute_resistance(self):
        """
        Compute the resistance limits
        :return:
        """
        pass


    def compute_indicators(self):
        """
        Compute all the relevant indicators
        :return:
        """
        self.update_quote_list()
        self.compute_bolinger_band()
        self.compute_macd()
        self.compute_rsi()



