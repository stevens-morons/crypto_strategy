import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import pyfolio as pf
import csv; import datetime; import pytz
from technical_indicators import BBANDS
from historical_data import exchange_data,write_to_csv,to_unix_time
import backtest

# ==========Initial trade parameters =============
symbol = 'BTC/USD'
timeframe = '1d'
trading_qty = 1.0
since = '2018-01-01 00:00:00'
hist_start_date = int(to_unix_time(since))
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
periods = 89

# ==========Initial exchange parameters =============
kraken = exchange_data('kraken','BTC/USD',timeframe=timeframe,since=hist_start_date)
write_to_csv(kraken,'BTC/USD','kraken')

data = pd.DataFrame(kraken,columns=header)
print(data.head())

# ============ Strategy Function - Exponential Moving average crossover ================
def strategy(data,periods):
    '''
    Strategy to buy/sell when price closes above/below EMA
    Default EMA chosen is 89 period EMA as historically
    found to give great results with most timeframes
    '''
    ema_short = data['Close'].ewm(span=periods, adjust=False).mean()

    # Difference between prices & EMA timeseries
    trading_positions_raw = data['Close'] - ema_short
    #trading_positions_raw.tail()

    # Taking the sign of the difference to determine whether the price or EMA is greater and then
    # multiply by qty

    trading_positions = trading_positions_raw.apply(np.sign)
    print('Trading Positions:', trading_positions.head())

    # Lagging our trading signals by one period
    trading_positions_final = trading_positions.shift(1) * trading_qty

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9))

    ax1.plot(data.loc[since:,:].index,data.loc[since:,'Close'],label = 'Price')
    ax1.plot(ema_short.loc[since:,:].index, ema_short.loc[since:,'Close'], label = "89 EMA")
    ax1.legend(loc='best')
    ax1.set_ylabel('Price($)')

    ax2.plot(trading_positions_final.loc[since:,:].index, trading_positions_final[since:,'Close'],
             label='Trading_Position')
    ax2.set_ylabel('Trading position')

    plt.show()

    data['returns'] = np.log(data['Close'].shift(1) / data['Close'])

    data['strat_returns'] = data['returns'] * trading_positions_final

    return data['strat_returns']

returns = strategy(data, periods)
backtest.drawdown_periods(returns)
backtest.underwater_plot(returns)
