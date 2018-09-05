import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyfolio as pf
import csv; import datetime; import pytz
from technical_indicators import BBANDS
from historical_data import exchange_data, write_to_csv, to_unix_time

symbol = 'BTC/USD'
timeframe = '1d'
since = '2017-01-01 00:00:00'
hist_start_date = int(to_unix_time(since))
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

kraken = exchange_data('kraken','BTC/USD',timeframe=timeframe,since=hist_start_date)
write_to_csv(kraken,'BTC/USD','kraken')
data = pd.DataFrame(kraken,columns=header)

# ===== Directional Backtesting platform using Pyfolio ======
# ======================================================================
'''
Functions for Drawdown Periods, Underwater plots, Monthly 
& Annual returns.
Create a comprehensive Tear sheet for strategy
'''
def drawdown_periods(returns):
    fig = plt.figure(facecolor='white')
    plt.yscale('log')
    ax = pf.plot_drawdown_periods(returns).set_xlabel('Date')
    plt.savefig('drawdown_periods.png')

def underwater_plot(returns):
    fig = plt.figure(facecolor='white')
    ax = pf.plot_drawdown_underwater(returns)
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
