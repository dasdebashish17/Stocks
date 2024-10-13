import datetime
from dateutil.relativedelta import relativedelta, FR, MO

import pandas as pd
import numpy as np
import re
from matplotlib import pyplot as plt
from nsepython import *

import plotly.graph_objects as go

from stock_indicators import indicators, Quote # https://python.stockindicators.dev/indicators/#content


class Fetch:
    """
    Class to fetch the stocks data from server
    """
    def __init__(self):
        self.series = 'EQ'

    def set_stock_symbol(self, symbol):
        """
        Set the stock symbol
        :param symbol: stock symbol
        :return:
        """
        self.stock_symbol = symbol


    def set_timeframe(self, weeks=90):
        """
        Set the timeframe for which stock data needs to be captured
        :return:
        """
        # get the datetime of Monday from specified weeks before
        end_date = datetime.date.today()
        start_date = end_date + relativedelta(weekday=MO(-weeks))
        ref_start_sunday = start_date + relativedelta(days=6)
        self.ref_sunday_list = [ref_start_sunday + relativedelta(days=7*week_idx) for week_idx in range(weeks)]
        # fetch upto latest date
        self.end_date = str(end_date.strftime("%d-%m-%Y"))
        # move back #days to get the start date
        self.start_date = str(start_date.strftime("%d-%m-%Y"))

    def get_day(self, date_str):
        year, month, date = date_str.split('-')
        dt = datetime.date(int(year), int(month), int(date))
        return dt.strftime("%A")

    def get_datetime(self, date_str):
        year, month, date = date_str.split('-')
        dt = datetime.date(int(year), int(month), int(date))
        return dt


    def fetch_data(self):
        """
        Fetch the historic data associated with the stock symbol
        """
        self.stock_df = equity_history(self.stock_symbol, self.series, self.start_date, self.end_date)
        if self.stock_df.empty:
            return None
        self.stock_df['WEEK_ID'] = -1
        self.stock_df = self.stock_df.sort_values('CH_TIMESTAMP')
        self.stock_df['WEEKDAY'] = self.stock_df['CH_TIMESTAMP'].apply(lambda x: self.get_day(x))
        self.stock_df['DATETIME'] = self.stock_df['CH_TIMESTAMP'].apply(lambda x: self.get_datetime(x))

        # iterate over all the rows, set WEEK_ID as 0 and keep incrementing whenever
        for idx in range(len(self.ref_sunday_list)):
            self.stock_df.loc[(self.stock_df['WEEK_ID'] == -1) & (self.stock_df['DATETIME'] < self.ref_sunday_list[idx]), 'WEEK_ID'] = idx

        return True

    def get_daily_data(self):
        """
        Get the daily stock data
        :return:
        """
        return self.stock_df


    def plot_data(self):
        """
        Plots the stock data
        """
        fig = go.Figure(data=[go.Candlestick(x=self.stock_df['CH_TIMESTAMP'],
                                             open=self.stock_df['CH_OPENING_PRICE'],
                                             high=self.stock_df['CH_TRADE_HIGH_PRICE'],
                                             low=self.stock_df['CH_TRADE_LOW_PRICE'],
                                             close=self.stock_df['CH_CLOSING_PRICE'])])

        fig.show()



if __name__ == '__main__':
    obj = Fetch()
    obj.set_stock_symbol("SBIN")
    obj.set_timeframe()
    obj.fetch_data()
    obj.plot_data()