import pandas as pd
import numpy as np
from time import time
import threading
import matplotlib.pyplot as plt
# import pyfolio as pf
import csv;
import datetime;
import pytz
from technical_indicators import BBANDS
from historical_data import exchange_data, write_to_csv, to_unix_time
# import backtest
import warnings
warnings.filterwarnings('ignore')

start = time()

# ==========Initial trade parameters =============
symbol = 'BTC/USD'
timeframe = '1d'
trn_cost = 0.0026       # === Transaction cost = 0.26%
borrow_cost = 0.0026    # === Assuming every short trade is 100 Hours
# since = '2017-01-01 00:00:00'
# hist_start_date = int(to_unix_time(since))
# header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

# ==========Initial exchange parameters =============
# kraken = exchange_data('kraken', 'BTC/USD', timeframe=timeframe, since=hist_start_date)
# write_to_csv(kraken, 'BTC/USD', 'kraken')
# data = pd.DataFrame(kraken, columns=header)
data = pd.read_csv("gemini_BTCUSD_1hr.csv")
# =================================================================
# ================ DIRECTIONAL STRATEGY ===========================
avg_true_range = ATR(data,24)
slippage = 0.0001 * avg_true_range['ATR'] # === Slippage as a function of Volatility
stddev = 2

def strategy(data, list_periods):
    '''
    :param data: dataframe with OHLCV
    :return: Strategy Returns and Equity Curve
    === Volatility Outburst Strategy ===
    Buy when Price closes above the Mean + default SD Value
    Sell when Price closes below the Mean - default SD Value
    '''

    data['returns'] = np.log(data['Close'].shift(1) / data['Close'])
    data['position'] = 0

    for period in list_periods:
        bbands = BBANDS(data, stddev, period)

        for row in range(len(data)):
            if data['position'].iloc[row] == 0:
                if data['Close'].iloc[row] > bbands['BB_Upper'].iloc[row]:
                    buy_price = data['Close'].iloc[row] * (1+trn_cost+slippage)
                    # print ("Bought at : "+ str(buy_price) +'\n')
                    data['position'] = 1

                elif data['Close'].iloc[row] < bbands['BB_Lower'].iloc[row]:
                    sell_price= data['Close'].iloc[row] * (1-trn_cost-slippage-borrow_cost)
                    data['position'] = -1
                    # data['strat_returns'] = sell_price / buy_price - 1

            elif data['position'].iloc[row] == 1:
                if data['Close'].iloc[row] < bbands['BB_Lower'].iloc[row]:
                    sell_price = data['Close'].iloc[row] * (1-trn_cost-slippage)
                    data['position'] = 0
                    data['strat_returns'] = sell_price / buy_price - 1

            elif data['position'].iloc[row] == -1:
                if data['Close'].iloc[row] > bbands['BB_Upper'].iloc[row]:
                    buy_price = data['Close'].iloc[row] * (1+trn_cost+slippage+borrow_cost)
                    data['position']= 0
                    data['strat_returns'] = sell_price/buy_price - 1

        # data['strat_returns'] = data['position'].shift(1) * data['returns']
        # print str(period) + "Period : " + data['strat_returns']
        cum_returns = data['strat_returns'].dropna().cumsum()
        print '\nCumulative Percentage Returns for ' + str(period) + ' period Volatility Burst: {}%'.format(round(cum_returns[-1:], 2))

    return data['strat_returns']

list_periods = range(10, 50, 5)
returns = strategy(data=data, list_periods=list_periods)
end = time()
print '\nTotal time for execution: {} secs '.format(round(end - start), 2)

# backtest.drawdown_periods(returns)
# backtest.underwater_plot(returns)
