import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import pyfolio as pf
from technical_indicators import RSI
from time import time
import warnings
warnings.filterwarnings('ignore')

start = time()
# ==========Initial trade parameters =============
symbol = 'BTC/USD'
timeframe = '1h'
trading_qty = 1.0
trn_cost = 0.0026       # === Transaction cost = 0.26%
slippage = 0.002        # === Slippage = 0.2%
borrow_cost = 0.0026    # === Assuming every short trade is 100 Hours
period = []

# ==========Initial exchange parameters =============
# kraken = exchange_data('kraken', 'BTC/USD', timeframe=timeframe, since=hist_start_date)
# write_to_csv(kraken, 'BTC/USD', 'kraken')
# data = pd.DataFrame(kraken, columns=header)
data = pd.read_csv("gemini_BTCUSD_1hr.csv")

# ============ Strategy Function - RSI as  Mean Reversion Indicator ================

buy_price = 0; sell_price = 0
data['returns'] = 0

def strategy(data):
    '''
    Buy when 'X' Period RSI crosses above the 0.10 level from below
    Sell when 'X' Period RSI crosses below the 0.90 level from above
    :param data: DataFrame with OHLC values
    :return: Cumulative Percentage returns
    '''

    # data['returns'] = np.log(data['Close'].shift(1)/data['Close'])
    data['position'] = 0
    data['strat_returns'] = 0

    for per in range(2,35,1):
        rsi_value = RSI(data, per)
        rsi_value.apply(pd.to_numeric,errors='ignore')
        for row in range(len(data)):
            if data['position'].iloc[row] == 0:
                if rsi_value['RSI'].iloc[row] > 0.10 and rsi_value['RSI'].iloc[row-1]<= 0.10:
                    buy_price = data['Close'].iloc[row] * (1+trn_cost+slippage)
                    # print ("Bought at : "+ str(buy_price) +'\n')
                    data['position'] = 1

                elif rsi_value['RSI'].iloc[row] < 0.90 and rsi_value['RSI'].iloc[row-1] >= 0.90:
                    sell_price= data['Close'].iloc[row] * (1-trn_cost-slippage-borrow_cost)
                    data['position'] = -1
                    # data['strat_returns'] = sell_price / buy_price - 1

            elif data['position'].iloc[row] == 1:
                if rsi_value['RSI'].iloc[row] < 0.90 and rsi_value['RSI'].iloc[row-1] >= 0.90:
                    sell_price = data['Close'].iloc[row] * (1-trn_cost-slippage)
                    data['position'] = 0
                    data['strat_returns'] = sell_price / buy_price - 1

            elif data['position'].iloc[row] == -1:
                if rsi_value['RSI'].iloc[row] > 0.10 and rsi_value['RSI'].iloc[row-1] <= 0.10:
                    buy_price = data['Close'].iloc[row] * (1+trn_cost+slippage+borrow_cost)
                    data['position'] = 0
                    data['strat_returns'] = sell_price/buy_price - 1


        # data['strat_returns'] = data['position'].shift(1) * data['returns']
        cum_returns = data['strat_returns'].dropna().cumsum()
        print '\nCumulative Percentage Returns for ' + str(per) +\
              ' period RSI Strategy: {}%'.format(round(cum_returns[-1:], 2))

    return data['strat_returns']


returns = strategy(data)
end = time()
print '\nTotal time for execution: {} secs '.format(round(end - start), 2)


