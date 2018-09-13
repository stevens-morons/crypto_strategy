import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import pyfolio as pf
import csv; import datetime; import pytz
from technical_indicators import BBANDS
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

def cdl_patterns(data):
    '''
    Open and close are near, low is much lower,
    hence tail or shadow is very long
    :param data:
    :return:
    '''
    for cdl in range(len(data)):
        '''
        Open and close are near, low is much lower,
        hence tail or shadow is very long
        '''
        doji = data['Close'].iloc[cdl] - data['Open'].iloc[cdl] > 3*(data['Low'] and






