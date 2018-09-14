import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import pyfolio as pf
from collections import deque
from historical_data import exchange_data, write_to_csv, to_unix_time
import threading
import warnings
warnings.filterwarnings('ignore')
from time import time

start = time()
# ==========Initial trade parameters =============
symbol = 'BTC/USD'
timeframe = '1d'
since = '2017-01-01 00:00:00'
hist_start_date = int(to_unix_time(since))
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

# ==========Initial exchange parameters =============
# kraken = exchange_data('kraken', 'BTC/USD', timeframe=timeframe, since=hist_start_date)
# write_to_csv(kraken,'BTC/USD','kraken')

# data = pd.DataFrame(kraken, columns=header)
# print(data.head())
data = pd.read_csv("gemini_BTCUSD_1hr.csv")


def avg_hl(data):
    hl_range = data['High'] - data['Low']
    avg_HL = pd.rolling_mean(hl_range, 30)
    return avg_HL

def hammer_pattern(data):
    '''
    Hammer - Open and close are near, low is much lower,
    hence tail or shadow is very long.
    Close is high or very near. Previous candle close is lower than open
    :param data:
    :return:
    '''
    trigger_candle = deque()
    for cdl in range(len(data)):
        cond_1 = (data['High'].iloc[cdl] - data['Low'].iloc[cdl]) >\
                 4*(data['Close'].iloc[cdl] - data['Open'].iloc[cdl])

        cond_2 = data['Close'].iloc[cdl] == data['High'].iloc[cdl]
        cond_3 = 2 * (data['High'].iloc[cdl] - data['Close'].iloc[cdl]) <\
                 data['Close'].iloc[cdl] - data['Open'].iloc[cdl]

        cond_4 = data['Close'].iloc[cdl-1] < data['Open'].iloc[cdl-1]
        hammer = cond_1 and cond_4 and (cond_2 or cond_3)

        if hammer:
            trigger_candle.append(data['High'].iloc[cdl])
            trigger_candle.append(data['Low'].iloc[cdl])

    return trigger_candle

def bull_candle(data):
    '''
    Incorporating both Bullish engulfing and Bullish Piercing
    Bullish Engulfing - Current candle Open is lower than Close of previous candle.
                        Close is higher than high of previous candle.
    Bullish Piercing - Current candle Open is lower than low of previous candle.
                        Close is more than 75% of (High-Low range of prev. candle)
    :param data:
    :return:
    '''
    trigger_candle_high = deque([])
    trigger_candle_low = deque([])
    for cdl in range(len(data)):
        cond_1 = data['Open'].iloc[cdl] < data['Close'].iloc[cdl-1]
        cond_2 = data['Close'].iloc[cdl] > data['High'].iloc[cdl-1]
        cond_3 = data['Close'].iloc[cdl] > 0.75*\
                                           (data['High'].iloc[cdl-1] - data['Low'].iloc[cdl-1])

        bull_cdl = cond_1 and (cond_2 or cond_3)

        if bull_cdl:
            trigger_candle_high.appendleft(data['High'].iloc[cdl])

            trigger_candle_low.appendleft(data['Low'].iloc[cdl])

    return trigger_price

def harami(data):
    '''
    Harami - In japanese, it means a woman who is visibly pregnant
    Previous candle is a long bearish one,
    :param data:
    :return:
    '''

    # ==== Incomplete ======







        
















