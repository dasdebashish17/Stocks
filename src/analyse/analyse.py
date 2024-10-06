import sys

try:
    from indicator.indicators import Indicator
except:
    from indicators import Indicator


class Analyse:
    def __init__(self):
        self.indicator_obj = Indicator()


    def set_data(self, stock_df):
        self.date = stock_df['CH_TIMESTAMP'].tolist()
        self.open_price = stock_df['CH_OPENING_PRICE'].tolist()
        self.high_price = stock_df['CH_TRADE_HIGH_PRICE'].tolist()
        self.low_price = stock_df['CH_TRADE_LOW_PRICE'].tolist()
        self.close_price = stock_df['CH_CLOSING_PRICE'].tolist()
        self.volume = stock_df['CH_TOT_TRADED_QTY'].tolist()

        self.indicator_obj.set_params(self.date, self.open_price, self.high_price, self.low_price, self.close_price, self.volume)
        self.indicator_obj.compute_indicators()


    def bolinger_band_analysis(self):
        """
        Check if the stock price has gone below the bolinger band limits
        :return:
        """
        buy_indicator = False
        lower_price = self.low_price[-1]
        close_price = self.close_price[-1]
        bolinger_band_lower_limit = self.indicator_obj.bolinger_band_data["lower_band"][-1]

        if (lower_price < 1.02 * bolinger_band_lower_limit):
            buy_indicator = True

        return buy_indicator



    def rsi_analysis(self):
        """
        Check if the stock price has gone below the bolinger band limits
        :return:
        """
        buy_indicator = False
        rsi_limit = self.indicator_obj.rsi_data[-1]
        if rsi_limit < 38:
            buy_indicator = True

        return buy_indicator


    def analyse_indicators(self):
        buy_indicator = False
        buy_indicator = buy_indicator | self.bolinger_band_analysis()
        buy_indicator = buy_indicator | self.rsi_analysis()

        return buy_indicator

