import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyfolio as pf
import csv; import datetime; import pytz
from technical_indicators import BBANDS
from historical_data import exchange_data,write_to_csv,to_unix_time
from empyrical.utils import nanmean
from zipline.utils import math_utils

symbol = 'BTC/USD'
timeframe = '1d'
since = '2017-01-01 00:00:00'
hist_start_date = int(to_unix_time(since))
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

kraken = exchange_data('kraken','BTC/USD',timeframe=timeframe,since=hist_start_date)
write_to_csv(kraken,'BTC/USD','kraken')
data = pd.DataFrame(kraken,columns=header)

# ===== Using Pyfolio Functions ======
def drawdown_periods(returns):
    fig = plt.figure(facecolor='white')
    plt.yscale('log')
    ax = pf.plot_drawdown_periods(returns).set_xlabel('Date')
    plt.savefig('drawdown_periods.png')

def underwater_plot(returns):
    fig = plt.figure(facecolor='white')
    ax=pf.plot_drawdown_underwater(returns)
    plt.savefig('underwater_plot.png')

def monthly_returns(returns):
    fig = plt.figure(facecolor='white')
    ax = pf.plot_monthly_returns_heatmap(returns)
    plt.savefig('monthly_returns.png')

def annual_returns(returns):
    fig = plt.figure(facecolor='white')
    ax = pf.plot_annual_returns(returns)
    plt.savefig('annual_returns.png')

def create_full_tear_sheet(returns):
    pf.create_full_tear_sheet(returns)

# =================================================================
# ================ DIRECTIONAL STRATEGY ===========================
stddev = 2; n = 20  # ====== parameters

# ==== Calling the function from technical_indicators.py ==========
bbands = BBANDS(data, stddev, n)

def strategy(data):
    buy = data['Close'] > bbands['BB_Upper20']
    sell = data['Close'] < bbands['BB_Lower20']

    data['returns'] = np.log(data['Close']/data['Close'].shift(1))

    for row in range(0,len(data)):
        if data[row]['Close'] > bbands[row]['BB_Upper20']:
            data[row]['position'] = 1
        elif data[row]['Close'] < bbands[row]['BB_Lower20']:
            data[row]['position'] = -1

    data['strat_returns'] = data['position'].shift(1) * data['returns']
    data['cum_returns'] = data['strat_returns'].dropna().cumsum().apply(np.exp)

    return data['strat_returns']
returns = strategy(data=data)
drawdown_periods(returns)
underwater_plot(returns)
