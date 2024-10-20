
import pandas as pd
import re
import datetime

class Resample:
    def __init__(self):
        pass

    def set_stock_df(self, stock_df):
        """
        Initializes the stock dataframe
        :param stock_df:
        {'data':
            [
                {'_id': '661e687fc1cb1b138131ff40',
                'CH_SYMBOL': 'SBIN',
                'CH_SERIES': 'EQ',
                'CH_MARKET_TYPE': 'N',
                'CH_TIMESTAMP': '2024-04-16',
                'TIMESTAMP': '2024-04-15T18:30:00.000Z',
                'CH_TRADE_HIGH_PRICE': 754.9,
                'CH_TRADE_LOW_PRICE': 744.4,
                'CH_OPENING_PRICE': 751.25,
                'CH_CLOSING_PRICE': 751.7,
                'CH_LAST_TRADED_PRICE': 752.8,
                'CH_PREVIOUS_CLS_PRICE': 757.5,
                'CH_TOT_TRADED_QTY': 13338991,
                'CH_TOT_TRADED_VAL': 10005242780,
                'CH_52WEEK_HIGH_PRICE': 793.4,
                'CH_52WEEK_LOW_PRICE': 528,
                'CH_TOTAL_TRADES': 202899,
                'CH_ISIN': 'INE062A01020',
                'createdAt': '2024-04-16T12:01:03.311Z',
                'updatedAt': '2024-04-16T12:01:03.311Z',
                '__v': 0,
                'SLBMH_TOT_VAL': None,
                'VWAP': 750.07,
                'mTIMESTAMP': '16-Apr-2024'
                },
                {'_id': '661d170667f74c7b05bb457a', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TRADE_HIGH_PRICE': 763.3, 'CH_TRADE_LOW_PRICE': 748.75, 'CH_OPENING_PRICE': 759.8, 'CH_CLOSING_PRICE': 757.5, 'CH_LAST_TRADED_PRICE': 758.9, 'CH_PREVIOUS_CLS_PRICE': 766.3, 'CH_TOT_TRADED_QTY': 11356572, 'CH_TOT_TRADED_VAL': 8595700637, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 528, 'CH_TOTAL_TRADES': 203154, 'CH_ISIN': 'INE062A01020', 'CH_TIMESTAMP': '2024-04-15', 'TIMESTAMP': '2024-04-14T18:30:00.000Z', 'createdAt': '2024-04-15T12:01:10.183Z', 'updatedAt': '2024-04-15T12:01:10.183Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 756.89, 'mTIMESTAMP': '15-Apr-2024'},
                {'_id': '661922600661c0c135aab630', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-04-12', 'TIMESTAMP': '2024-04-11T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 779.5, 'CH_TRADE_LOW_PRICE': 764.8, 'CH_OPENING_PRICE': 777.25, 'CH_CLOSING_PRICE': 766.3, 'CH_LAST_TRADED_PRICE': 766.55, 'CH_PREVIOUS_CLS_PRICE': 779.05, 'CH_TOT_TRADED_QTY': 14408722, 'CH_TOT_TRADED_VAL': 11128157762.8, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 524.4, 'CH_TOTAL_TRADES': 245294, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-04-12T12:00:32.869Z', 'updatedAt': '2024-04-12T12:00:32.869Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 772.32, 'mTIMESTAMP': '12-Apr-2024'},
                {'_id': '66167f6f10604a87b12eb14f', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TRADE_HIGH_PRICE': 780.7, 'CH_TRADE_LOW_PRICE': 763.65, 'CH_OPENING_PRICE': 766.5, 'CH_CLOSING_PRICE': 779.05, 'CH_LAST_TRADED_PRICE': 777.4, 'CH_PREVIOUS_CLS_PRICE': 764.2, 'CH_TOT_TRADED_QTY': 14530669, 'CH_TOT_TRADED_VAL': 11230749541.1, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 524.4, 'CH_TOTAL_TRADES': 201570, 'CH_ISIN': 'INE062A01020', 'CH_TIMESTAMP': '2024-04-10', 'TIMESTAMP': '2024-04-09T18:30:00.000Z', 'createdAt': '2024-04-10T12:00:47.583Z', 'updatedAt': '2024-04-10T12:00:47.583Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 772.9, 'mTIMESTAMP': '10-Apr-2024'},
                {'_id': '661551ec5e9189ad01de7cf9', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-04-09', 'TIMESTAMP': '2024-04-08T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 772.45, 'CH_TRADE_LOW_PRICE': 761.1, 'CH_OPENING_PRICE': 768.45, 'CH_CLOSING_PRICE': 764.2, 'CH_LAST_TRADED_PRICE': 765.05, 'CH_PREVIOUS_CLS_PRICE': 768.3, 'CH_TOT_TRADED_QTY': 7465892, 'CH_TOT_TRADED_VAL': 5724766013.05, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 524.4, 'CH_TOTAL_TRADES': 127868, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-04-09T14:34:20.924Z', 'updatedAt': '2024-04-09T14:34:20.924Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 766.79, 'mTIMESTAMP': '09-Apr-2024'},
                {'_id': '6613dc7f0e60a36f852fb5e1', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-04-08', 'TIMESTAMP': '2024-04-07T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 770, 'CH_TRADE_LOW_PRICE': 761.8, 'CH_OPENING_PRICE': 766.05, 'CH_CLOSING_PRICE': 768.3, 'CH_LAST_TRADED_PRICE': 767.6, 'CH_PREVIOUS_CLS_PRICE': 764.75, 'CH_TOT_TRADED_QTY': 9797174, 'CH_TOT_TRADED_VAL': 7504931342.05, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 524.4, 'CH_TOTAL_TRADES': 193392, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-04-08T12:01:03.791Z', 'updatedAt': '2024-04-08T12:01:03.791Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 766.03, 'mTIMESTAMP': '08-Apr-2024'},
                {'_id': '661017bfb972bf436f4115cd', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TRADE_HIGH_PRICE': 767.7, 'CH_TRADE_LOW_PRICE': 752.6, 'CH_OPENING_PRICE': 757.95, 'CH_CLOSING_PRICE': 764.75, 'CH_LAST_TRADED_PRICE': 765.9, 'CH_PREVIOUS_CLS_PRICE': 759.3, 'CH_TOT_TRADED_QTY': 9939620, 'CH_TOT_TRADED_VAL': 7557966836.05, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 519.05, 'CH_TOTAL_TRADES': 159848, 'CH_ISIN': 'INE062A01020', 'CH_TIMESTAMP': '2024-04-05', 'TIMESTAMP': '2024-04-04T18:30:00.000Z', 'createdAt': '2024-04-05T15:24:47.951Z', 'updatedAt': '2024-04-05T15:24:47.951Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 760.39, 'mTIMESTAMP': '05-Apr-2024'},
                {'_id': '660e96864c86b12e15540d6b', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TRADE_HIGH_PRICE': 775.3, 'CH_TRADE_LOW_PRICE': 758.1, 'CH_OPENING_PRICE': 775, 'CH_CLOSING_PRICE': 759.3, 'CH_LAST_TRADED_PRICE': 760.8, 'CH_PREVIOUS_CLS_PRICE': 771.05, 'CH_TOT_TRADED_QTY': 15889530, 'CH_TOT_TRADED_VAL': 12127483574.7, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 519.05, 'CH_TOTAL_TRADES': 263762, 'CH_ISIN': 'INE062A01020', 'CH_TIMESTAMP': '2024-04-04', 'TIMESTAMP': '2024-04-03T18:30:00.000Z', 'createdAt': '2024-04-04T12:01:10.542Z', 'updatedAt': '2024-04-04T12:01:10.542Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 763.24, 'mTIMESTAMP': '04-Apr-2024'},
                {'_id': '660d4512d68c6c75db4e9afb', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TRADE_HIGH_PRICE': 772.6, 'CH_TRADE_LOW_PRICE': 760.15, 'CH_OPENING_PRICE': 764.9, 'CH_CLOSING_PRICE': 771.05, 'CH_LAST_TRADED_PRICE': 771, 'CH_PREVIOUS_CLS_PRICE': 766.4, 'CH_TOT_TRADED_QTY': 19136981, 'CH_TOT_TRADED_VAL': 14694203509.3, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 519.05, 'CH_TOTAL_TRADES': 277412, 'CH_ISIN': 'INE062A01020', 'CH_TIMESTAMP': '2024-04-03', 'TIMESTAMP': '2024-04-02T18:30:00.000Z', 'createdAt': '2024-04-03T12:01:22.504Z', 'updatedAt': '2024-04-03T12:01:22.504Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 767.84, 'mTIMESTAMP': '03-Apr-2024'},
                {'_id': '660bf35c4a76eba9c31e1a17', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-04-02', 'TIMESTAMP': '2024-04-01T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 768.75, 'CH_TRADE_LOW_PRICE': 753.35, 'CH_OPENING_PRICE': 758.2, 'CH_CLOSING_PRICE': 766.4, 'CH_LAST_TRADED_PRICE': 765.95, 'CH_PREVIOUS_CLS_PRICE': 758.3, 'CH_TOT_TRADED_QTY': 15713063, 'CH_TOT_TRADED_VAL': 11967515949.7, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 519.05, 'CH_TOTAL_TRADES': 199522, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-04-02T12:00:28.653Z', 'updatedAt': '2024-04-02T12:00:28.653Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 761.63, 'mTIMESTAMP': '02-Apr-2024'},
                {'_id': '660aa1ffb6a351c2ba40d514', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-04-01', 'TIMESTAMP': '2024-03-31T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 761.5, 'CH_TRADE_LOW_PRICE': 752.1, 'CH_OPENING_PRICE': 759.05, 'CH_CLOSING_PRICE': 758.3, 'CH_LAST_TRADED_PRICE': 758, 'CH_PREVIOUS_CLS_PRICE': 752.35, 'CH_TOT_TRADED_QTY': 9949971, 'CH_TOT_TRADED_VAL': 7533678627.05, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 519.05, 'CH_TOTAL_TRADES': 155072, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-04-01T12:01:03.274Z', 'updatedAt': '2024-04-01T12:01:03.274Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 757.16, 'mTIMESTAMP': '01-Apr-2024'},
                {'_id': '66055bff7a3e097b6f858a87', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-28', 'TIMESTAMP': '2024-03-27T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 759.55, 'CH_TRADE_LOW_PRICE': 736.9, 'CH_OPENING_PRICE': 737.75, 'CH_CLOSING_PRICE': 752.35, 'CH_LAST_TRADED_PRICE': 752.95, 'CH_PREVIOUS_CLS_PRICE': 733.3, 'CH_TOT_TRADED_QTY': 21705116, 'CH_TOT_TRADED_VAL': 16296764834.75, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 250615, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-28T12:01:03.696Z', 'updatedAt': '2024-03-28T12:01:03.696Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 750.83, 'mTIMESTAMP': '28-Mar-2024'},
                {'_id': '66040cccf79bf22bf30dfd8b', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TRADE_HIGH_PRICE': 745.85, 'CH_TRADE_LOW_PRICE': 730.2, 'CH_OPENING_PRICE': 743, 'CH_CLOSING_PRICE': 733.3, 'CH_LAST_TRADED_PRICE': 736.5, 'CH_PREVIOUS_CLS_PRICE': 740.05, 'CH_TOT_TRADED_QTY': 30088789, 'CH_TOT_TRADED_VAL': 22142632347.65, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 303834, 'CH_ISIN': 'INE062A01020', 'CH_TIMESTAMP': '2024-03-27', 'TIMESTAMP': '2024-03-26T18:30:00.000Z', 'createdAt': '2024-03-27T12:10:52.971Z', 'updatedAt': '2024-03-27T12:10:52.971Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 735.91, 'mTIMESTAMP': '27-Mar-2024'},
                {'_id': '6602db38f04eb262462f60e0', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-26', 'TIMESTAMP': '2024-03-25T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 747.85, 'CH_TRADE_LOW_PRICE': 738.5, 'CH_OPENING_PRICE': 743.05, 'CH_CLOSING_PRICE': 740.05, 'CH_LAST_TRADED_PRICE': 741.8, 'CH_PREVIOUS_CLS_PRICE': 746.7, 'CH_TOT_TRADED_QTY': 14678342, 'CH_TOT_TRADED_VAL': 10878801267.1, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 471853, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-26T14:27:04.122Z', 'updatedAt': '2024-03-26T14:27:04.122Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 741.15, 'mTIMESTAMP': '26-Mar-2024'},
                {'_id': '65fd72dcb19be7cbf8a594ea', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-22', 'TIMESTAMP': '2024-03-21T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 748.8, 'CH_TRADE_LOW_PRICE': 741.4, 'CH_OPENING_PRICE': 743.85, 'CH_CLOSING_PRICE': 746.7, 'CH_LAST_TRADED_PRICE': 746.5, 'CH_PREVIOUS_CLS_PRICE': 744.3, 'CH_TOT_TRADED_QTY': 15535921, 'CH_TOT_TRADED_VAL': 11591196217.5, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 261750, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-22T12:00:28.075Z', 'updatedAt': '2024-03-22T12:00:28.075Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 746.09, 'mTIMESTAMP': '22-Mar-2024'},
                {'_id': '65fc217fac280a1df6bcea43', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-21', 'TIMESTAMP': '2024-03-20T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 750.6, 'CH_TRADE_LOW_PRICE': 740.55, 'CH_OPENING_PRICE': 742, 'CH_CLOSING_PRICE': 744.3, 'CH_LAST_TRADED_PRICE': 742.8, 'CH_PREVIOUS_CLS_PRICE': 736.25, 'CH_TOT_TRADED_QTY': 15161161, 'CH_TOT_TRADED_VAL': 11300817864, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 297397, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-21T12:01:03.438Z', 'updatedAt': '2024-03-21T12:01:03.438Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 745.38, 'mTIMESTAMP': '21-Mar-2024'},
                {'_id': '65facfde875450dd912113bc', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-20', 'TIMESTAMP': '2024-03-19T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 738.95, 'CH_TRADE_LOW_PRICE': 719.8, 'CH_OPENING_PRICE': 725.15, 'CH_CLOSING_PRICE': 736.25, 'CH_LAST_TRADED_PRICE': 736.6, 'CH_PREVIOUS_CLS_PRICE': 723.8, 'CH_TOT_TRADED_QTY': 25405455, 'CH_TOT_TRADED_VAL': 18575665608.1, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 411626, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-20T12:00:30.744Z', 'updatedAt': '2024-03-20T12:00:30.744Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 731.17, 'mTIMESTAMP': '20-Mar-2024'},
                {'_id': '65f97e7f498fc9e8676101d1', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-19', 'TIMESTAMP': '2024-03-18T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 734.35, 'CH_TRADE_LOW_PRICE': 721.15, 'CH_OPENING_PRICE': 730, 'CH_CLOSING_PRICE': 723.8, 'CH_LAST_TRADED_PRICE': 722.55, 'CH_PREVIOUS_CLS_PRICE': 730.95, 'CH_TOT_TRADED_QTY': 15205043, 'CH_TOT_TRADED_VAL': 11061261059.95, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 203852, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-19T12:01:03.617Z', 'updatedAt': '2024-03-19T12:01:03.617Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 727.47, 'mTIMESTAMP': '19-Mar-2024'},
                {'_id': '65f82cdd232b4b49d1020606', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-18', 'TIMESTAMP': '2024-03-17T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 737.9, 'CH_TRADE_LOW_PRICE': 722.1, 'CH_OPENING_PRICE': 727.1, 'CH_CLOSING_PRICE': 730.95, 'CH_LAST_TRADED_PRICE': 732.45, 'CH_PREVIOUS_CLS_PRICE': 731.9, 'CH_TOT_TRADED_QTY': 18145126, 'CH_TOT_TRADED_VAL': 13242520782.95, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 266091, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-18T12:00:29.949Z', 'updatedAt': '2024-03-18T12:00:29.949Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 729.81, 'mTIMESTAMP': '18-Mar-2024'},
                {'_id': '65f4387f449d8ee9fc013122', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-15', 'TIMESTAMP': '2024-03-14T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 746.55, 'CH_TRADE_LOW_PRICE': 723, 'CH_OPENING_PRICE': 739.25, 'CH_CLOSING_PRICE': 731.9, 'CH_LAST_TRADED_PRICE': 732.65, 'CH_PREVIOUS_CLS_PRICE': 741.05, 'CH_TOT_TRADED_QTY': 29792241, 'CH_TOT_TRADED_VAL': 21786099985.35, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 382516, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-15T12:01:03.867Z', 'updatedAt': '2024-03-15T12:01:03.867Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 731.27, 'mTIMESTAMP': '15-Mar-2024'},
                {'_id': '65f2e6ffba531f76a2e97a8b', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-14', 'TIMESTAMP': '2024-03-13T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 750.8, 'CH_TRADE_LOW_PRICE': 734.05, 'CH_OPENING_PRICE': 749.9, 'CH_CLOSING_PRICE': 741.05, 'CH_LAST_TRADED_PRICE': 741, 'CH_PREVIOUS_CLS_PRICE': 747.25, 'CH_TOT_TRADED_QTY': 19730882, 'CH_TOT_TRADED_VAL': 14660690669.7, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 304735, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-14T12:01:03.280Z', 'updatedAt': '2024-03-14T12:01:03.280Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 743.03, 'mTIMESTAMP': '14-Mar-2024'},
                {'_id': '65f19562e2a16978fb6ca68d', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-13', 'TIMESTAMP': '2024-03-12T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 763.7, 'CH_TRADE_LOW_PRICE': 743, 'CH_OPENING_PRICE': 758.65, 'CH_CLOSING_PRICE': 747.25, 'CH_LAST_TRADED_PRICE': 747.4, 'CH_PREVIOUS_CLS_PRICE': 759.7, 'CH_TOT_TRADED_QTY': 27950252, 'CH_TOT_TRADED_VAL': 21014317799.65, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 462302, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-13T12:00:34.262Z', 'updatedAt': '2024-03-13T12:00:34.262Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 751.85, 'mTIMESTAMP': '13-Mar-2024'},
                {'_id': '65f043de249c86c7a88fa5df', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-12', 'TIMESTAMP': '2024-03-11T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 777.75, 'CH_TRADE_LOW_PRICE': 757.35, 'CH_OPENING_PRICE': 770, 'CH_CLOSING_PRICE': 759.7, 'CH_LAST_TRADED_PRICE': 759, 'CH_PREVIOUS_CLS_PRICE': 773.7, 'CH_TOT_TRADED_QTY': 21529705, 'CH_TOT_TRADED_VAL': 16463045923.05, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 390497, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-12T12:00:30.371Z', 'updatedAt': '2024-03-12T12:00:30.371Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 764.67, 'mTIMESTAMP': '12-Mar-2024'},
                {'_id': '65ef05b7646a0fb86a14310f', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-11', 'TIMESTAMP': '2024-03-10T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 792.8, 'CH_TRADE_LOW_PRICE': 770.55, 'CH_OPENING_PRICE': 790, 'CH_CLOSING_PRICE': 773.7, 'CH_LAST_TRADED_PRICE': 773.95, 'CH_PREVIOUS_CLS_PRICE': 788.05, 'CH_TOT_TRADED_QTY': 16778340, 'CH_TOT_TRADED_VAL': 13063454668.35, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 387291, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-11T13:23:03.057Z', 'updatedAt': '2024-03-11T13:23:03.057Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 778.59, 'mTIMESTAMP': '11-Mar-2024'},
                {'_id': '65e9ac7e3d2532dd72f7bb31', 'CH_SYMBOL': 'SBIN', 'CH_SERIES': 'EQ', 'CH_MARKET_TYPE': 'N', 'CH_TIMESTAMP': '2024-03-07', 'TIMESTAMP': '2024-03-06T18:30:00.000Z', 'CH_TRADE_HIGH_PRICE': 793.4, 'CH_TRADE_LOW_PRICE': 783, 'CH_OPENING_PRICE': 790, 'CH_CLOSING_PRICE': 788.05, 'CH_LAST_TRADED_PRICE': 786, 'CH_PREVIOUS_CLS_PRICE': 783.9, 'CH_TOT_TRADED_QTY': 15497868, 'CH_TOT_TRADED_VAL': 12220705592.6, 'CH_52WEEK_HIGH_PRICE': 793.4, 'CH_52WEEK_LOW_PRICE': 501.55, 'CH_TOTAL_TRADES': 219629, 'CH_ISIN': 'INE062A01020', 'createdAt': '2024-03-07T12:01:02.960Z', 'updatedAt': '2024-03-07T12:01:02.960Z', '__v': 0, 'SLBMH_TOT_VAL': None, 'VWAP': 788.54, 'mTIMESTAMP': '07-Mar-2024'}
            ],

            'meta': {
                'series': ['EQ'],
                'fromDate': '07-03-2024',
                'toDate': '16-04-2024',
                'symbols': ['SBIN', 'SBIN']}}

        :return:
        """
        self.stock_df = stock_df


    def resample_weekly(self):
        """
        relevant columns
        'WEEK_ID',
        'CH_TIMESTAMP': '2024-04-16',       start
        'CH_TRADE_HIGH_PRICE': 754.9,       max
        'CH_TRADE_LOW_PRICE': 744.4,        min
        'CH_OPENING_PRICE': 751.25,         start
        'CH_CLOSING_PRICE': 751.7,          last
        'CH_TOT_TRADED_QTY': 13338991,      sum
        'CH_TOT_TRADED_VAL': 10005242780,   sum
        'CH_TOTAL_TRADES': 202899,          sum
        'VWAP': 750.07

        :return:
        """
        # get the first entry from stock_df.
        columns = ['WEEK_ID', 'CH_TIMESTAMP', 'CH_TRADE_HIGH_PRICE', 'CH_TRADE_LOW_PRICE', 'CH_OPENING_PRICE',
                   'CH_CLOSING_PRICE', 'CH_TOT_TRADED_QTY', 'CH_TOT_TRADED_VAL', 'CH_TOTAL_TRADES', 'VWAP']

        self.stock_df_weekly = pd.DataFrame(columns = columns)

        num_weeks = max(self.stock_df['WEEK_ID']) + 1

        for week_id in range(num_weeks):
            df_local = self.stock_df.query(f"WEEK_ID == {week_id}")
            if df_local.empty:
                continue
            CH_TIMESTAMP = df_local['CH_TIMESTAMP'].tolist()[0]
            CH_TRADE_HIGH_PRICE = max(df_local['CH_TRADE_HIGH_PRICE'])
            CH_TRADE_LOW_PRICE = min(df_local['CH_TRADE_LOW_PRICE'])
            CH_OPENING_PRICE = df_local['CH_OPENING_PRICE'].tolist()[0]
            CH_CLOSING_PRICE = df_local['CH_CLOSING_PRICE'].tolist()[-1]
            CH_TOT_TRADED_QTY = sum(df_local['CH_TOT_TRADED_QTY'])
            CH_TOT_TRADED_VAL = sum(df_local['CH_TOT_TRADED_VAL'])
            CH_TOTAL_TRADES = sum(df_local['CH_TOTAL_TRADES'])
            VWAP = sum(df_local['VWAP'])
            new_row = pd.Series({"WEEK_ID": week_id, "CH_TIMESTAMP": CH_TIMESTAMP, "CH_TRADE_HIGH_PRICE": CH_TRADE_HIGH_PRICE,
                                 "CH_TRADE_LOW_PRICE": CH_TRADE_LOW_PRICE, "CH_OPENING_PRICE": CH_OPENING_PRICE,
                                 "CH_CLOSING_PRICE": CH_CLOSING_PRICE, "CH_TOT_TRADED_QTY": CH_TOT_TRADED_QTY,
                                 "CH_TOT_TRADED_VAL": CH_TOT_TRADED_VAL, "CH_TOTAL_TRADES": CH_TOTAL_TRADES,
                                 "VWAP": VWAP})

            self.stock_df_weekly = self.stock_df_weekly._append(new_row, ignore_index=True)

            pass


    def get_weekly_data(self):
        """
        Get the weekly data
        :return:
        """
        return self.stock_df_weekly





"""
In a new class Analytics(), we first find the stocks which have crossed their lower bound of Bollinger Band indicating best buy.
Another class will be needed which provides the support and resistance limits for any given time series data. This will help to 
find the support and resistance for the stock price/Bolinger band/RSI for daily and weekly stock price.

"""