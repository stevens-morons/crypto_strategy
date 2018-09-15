import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import pyfolio as pf
import csv; import datetime; import pytz
from technical_indicators import DONCH
from historical_data import exchange_data,write_to_csv,to_unix_time
# import backtest
import warnings
warnings.filterwarnings('ignore')

# ==========Initial trade parameters =============
symbol = 'BTC/USD'
timeframe = '1h'
trading_qty = 1.0
since = '2018-01-01 00:00:00'
hist_start_date = int(to_unix_time(since))
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
period = []

# ==========Initial exchange parameters =============
# kraken = exchange_data('kraken', 'BTC/USD', timeframe=timeframe, since=hist_start_date)
# write_to_csv(kraken, 'BTC/USD', 'kraken')
# data = pd.DataFrame(kraken, columns=header)
data = pd.read_csv("gemini_BTCUSD_1hr.csv")

# ============ Strategy Function - Donchian Bands crossover ================

buy_price = 0; sell_price = 0
data['returns'] = 0

def strategy(data):

    # data['returns'] = np.log(data['Close'].shift(1)/data['Close'])
    data['position'] = 0
    data['strat_returns'] = 0

    for per in range(20,100,5):
        upper_donch, lower_donch = DONCH(data, per)
        for row in range(len(data)):
            if data['position'].iloc[row] == 0:
                if data['Close'].iloc[row] > upper_donch.iloc[row]:
                    buy_price = data['Close'].iloc[row]
                    # print ("Bought at : "+ str(buy_price) +'\n')
                    data['position'] = 1

                elif data['Close'].iloc[row] < lower_donch.iloc[row]:
                    sell_price= data['Close'].iloc[row]
                    data['position'] = -1
                    # data['strat_returns'] = sell_price / buy_price - 1

            elif data['position'].iloc[row] == 1:
                if data['Close'].iloc[row] < lower_donch.iloc[row]:
                    sell_price = data['Close'].iloc[row]
                    data['position'] = 0
                    data['strat_returns'] = sell_price / buy_price - 1

            elif data['position'].iloc[row] == -1:
                if data['Close'].iloc[row] > upper_donch.iloc[row]:
                    buy_price = data['Close'].iloc[row]
                    data['position']= 0
                    data['strat_returns'] = sell_price/buy_price - 1


        # data['strat_returns'] = data['position'].shift(1) * data['returns']
        cum_returns = data['strat_returns'].dropna().cumsum()
        print 'Cumulative Percentage Returns for ' + str(per) + 'period Donchian: {}%'.format(round(cum_returns[-1:],2))

    return data['strat_returns']

returns = strategy(data)
# print returns,equity_curve
# backtest.drawdown_periods(returns)
# backtest.underwater_plot(returns)
