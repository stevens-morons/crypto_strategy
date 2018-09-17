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
symbol_list = ['BTC/USD', 'ETH/USD']
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

def main():
    while exchange.fetch_balance() > 0:
        for sym in symbol_list:
            init_macross(exchange, sym)

            oms.trade_details(sym)
            oms.exchange_balances()
    time.sleep(60)

# ===================== Data for various Timeframes ==========================
data_1m = exchange_data(exchange_id, symbol, timeframe='1m', since=start_date)
data_5m = exchange_data(exchange_id, symbol, timeframe='5m', since=start_date)
data_15m = exchange_data(exchange_id, symbol, timeframe='15m', since=start_date)
data_30m = exchange_data(exchange_id, symbol, timeframe='30m', since=start_date)
data_1hr = exchange_data(exchange_id, symbol, timeframe='1hr', since=start_date)
data_4hr = exchange_data(exchange_id, symbol, timeframe='4hr', since=start_date)


# =============== Strategy 1 - Moving average crossover =================
def init_macross(exchange,symbol):
    ema_short = strat_movavgcross.ema(data_1m, ema_period)
    bid, ask = oms.order_book(exchange, symbol, 5)
    buy_condition = bid > ema_short
    sell_condition = ask < ema_short

    init_qty = oms.position_dollar_value(symbol, per_trade_alloc=0.05, timeframe='1m') / oms.mid_price(exchange,symbol)
    init_trade = oms.create_trade(exchange, symbol, qty=init_qty)
    exit_trade = oms.closeout_trade(exchange, symbol, qty=init_qty)



# =============== Strategy 2  ================================
'''
Details of Strategy 2
'''

# =============== Strategy 3  ================================
'''
Details of Strategy 3
'''

if __name__=='__main__':
    main()


