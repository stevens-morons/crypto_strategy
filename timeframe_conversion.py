import numpy as np
import pandas as pd
from datetime import datetime

data = pd.read_csv('gemini_BTCUSD_2018_1min.csv')
data = data.drop('Unix Timestamp', axis=1)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Conversion method:
# Open = open of the first minute in n minute interval
# High = highest price in n minute interval
# Low = lowest price in n min interval
# Close = close of the last minute in n minute interval
# Volume = sum of volume for each minute in n minute interval


ohlc_dict = {                                                                                                             
'Open':'first',                                                                                                    
'High':'max',                                                                                                       
'Low':'min',                                                                                                        
'Close': 'last',                                                                                                    
'Volume': 'sum'
}

data_5m = data.resample('5T', how=ohlc_dict, closed='left', label='left')
data_10m = data.resample('10T', how=ohlc_dict, closed='left', label='left')
data_15m = data.resample('15T', how=ohlc_dict, closed='left', label='left')
data_30m = data.resample('30T', how=ohlc_dict, closed='left', label='left')
data_60m = data.resample('60T', how=ohlc_dict, closed='left', label='left')
data_120m = data.resample('120T', how=ohlc_dict, closed='left', label='left')
data_240m = data.resample('240T', how=ohlc_dict, closed='left', label='left')


data.to_csv('gemini_BTCUSD_2018_5min.csv')
data.to_csv('gemini_BTCUSD_2018_10min.csv')
data.to_csv('gemini_BTCUSD_2018_15min.csv')
data.to_csv('gemini_BTCUSD_2018_30min.csv')
data.to_csv('gemini_BTCUSD_2018_60min.csv')
data.to_csv('gemini_BTCUSD_2018_120min.csv')
data.to_csv('gemini_BTCUSD_2018_240min.csv')
