import ccxt
import datetime
import time
import math
# import pandas as pd
import numpy as np
import pprint

exchange_id = 'okex'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'timeout': 30000,
    'enableRateLimit': True,
})


# ======== Trading Qty Parameters =========
balance = 500 # Dollar amount
perc_trading_size = 0.25 # How much % of portfolio allocated to every trade


# ========= Visualise market depth ==========
def order_book(exchange, symbol, limit):
    # exchange = getattr(ccxt, exchange)()
    # exchange.load_markets()
    data = exchange.fetch_order_book(symbol,limit)
    bid = data['bids'][0][0] if len(data['bids']) > 0 else None
    ask = data['asks'][0][0] if len(data['asks']) > 0 else None
    return bid, ask


# ========= Mimicking close price as avg of bid-ask ===========
def mid_price(exchange, symbol):
    bid,ask = order_book(exchange, symbol, 5)
    mid_price = (bid+ask)/2
    return mid_price


# ========= Create Buy/Sell Orders when strategy conditions are satisfied ==========
def create_trade(exchange, symbol):
    buy_condition = False
    sell_condition = False

    qty = balance * perc_trading_size/mid_price(exchange,symbol)
    while len(exchange.private_post_positions()) == 0:
        if buy_condition:
            buy_order = exchange.create_limit_buy_order(symbol, qty,
                                                        order_book(exchange, symbol, 5)[1])
            print '{}'.format(symbol) + 'Buy Order created at:', buy_order['price']
        elif sell_condition:
            sell_order = exchange.create_limit_sell_order(symbol, qty,
                                                          order_book(exchange, symbol, 5)[0])
            print '{}'.format(symbol) + 'Sell Order created at:', sell_order['price']


# ========== Create strategy exit orders ================
def closeout_trade(exchange, symbol):
    buy_condition = False
    sell_condition = False

    qty = balance * perc_trading_size / mid_price(exchange, symbol)
    while exchange.private_post_positions() > 0:
        if exchange.private_post_positions()['side'] == 'buy' and sell_condition:
            close_buy = exchange.create_limit_sell_order(symbol, qty,
                                                         order_book(exchange, symbol, 5)[0])
            print '{}'.format(symbol) + 'Sell Order created at:', close_buy['price']

        elif exchange.private_post_positions()['side'] == 'sell' and buy_condition:
            close_sell = exchange.create_limit_buy_order(symbol, qty,
                                                         order_book(exchange, symbol, 5)[1])
            print '{}'.format(symbol) + 'Buy Order created at:', close_sell['price']


# ======== Details of Open & Closed Trades =========
def trade_details(symbol):
    print("Closed Orders:")
    pprint.pprint(exchange.fetch_closed_orders(symbol))

    print("Open Orders:")
    pprint.pprint(exchange.fetch_open_orders(symbol))


# ==== Get Balance amounts left on exchange =====
def exchange_balances():
    balance = exchange.fetch_balance()
    print 'Exchange Balance:\n', balance
