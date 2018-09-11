import ccxt
import datetime
import time
import math
# import pandas as pd
import numpy as np
import pprint
from historical_data import exchange_data
import oms

# ==== Initial exchange parameters =====
symbol = str('BTC/USD')
symbol_list = ['BTC/USD','ETH/USD']
timeframe = str('1d')
# exchange = str('okex')
start_date = str('2018-01-01')
get_data = True
ema_period = 100

exchange_id = 'kraken'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'timeout': 30000,
    'enableRateLimit': True,
})

# =============== Strategy 1 - Moving average crossover =================
data_macross = exchange_data(exchange_id, symbol, timeframe='1m', since=start_date)
def init_macross(exchange,symbol):
    ema_short = strat_movavgcross.ema(data_macross, ema_period)
    bid, ask = oms.order_book(exchange, symbol, 5)
    buy_condition = bid > ema_short
    sell_condition = ask < ema_shor

    init_trade = oms.create_trade(exchange, symbol)
    exit_trade = oms.closeout_trade(exchange, symbol)


# =============== Strategy 2  ================================
'''
Details of Strategy 2
'''

# =============== Strategy 3  ================================
'''
Details of Strategy 3
'''
