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
kraken = exchange_data('kraken', 'BTC/USD', timeframe=timeframe, since=hist_start_date)
write_to_csv(kraken,'BTC/USD','kraken')

data = pd.DataFrame(kraken, columns=header)
print(data.head())

# ============ Strategy Function - Donchian Bands crossover ================

def strategy(data):

    data['returns'] = np.log(data['Close'].shift(1)/data['Close'])
    data['position'] = 0

    for per in range(20,100,20):
        upper_donch, lower_donch = DONCH(data, per)
        for row in range(1, len(data)):
            if data['Close'].iloc[row] > upper_donch.iloc[row]:
                data['position'].iloc[row] = 1
            elif data['Close'].iloc[row] < lower_donch.iloc[row]:
                data['position'].iloc[row] = -1

            while data['position'].iloc[row - 1] == 1 and data['Close'].iloc[row] > lower_donch.iloc[row]:
                data['position'].iloc[row] = 1

            while (data['position'].iloc[row - 1] == -1) and (data['Close'].iloc[row] < upper_donch.iloc[row]):
                data['position'].iloc[row] = -1

        data['strat_returns'] = data['position'].shift(1) * data['returns']
        cum_returns = data['strat_returns'].dropna().cumsum().apply(np.exp)
        # print cum_returns

    return data['strat_returns'], cum_returns

# import Queue
# import threading
#
# data = Queue.Queue()
#
# for pr in range(20,100,5):
#     t = threading.Thread(target=strategy,args=(data))
#     t.daemon = True
#     t.start()
# s = data.get()
# print s
returns,equity_curve = strategy(data)
print returns,equity_curve
# backtest.drawdown_periods(returns)
# backtest.underwater_plot(returns)
