import pandas as pd
from datetime import datetime

data = pd.read_csv('gemini_BTCUSD_2018_1min.csv')
data = data.drop('Unix Timestamp', axis=1)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
exchange = 'gemini'
pair = 'BTCUSD'

# Conversion method:
# Open = open of the first minute in n minute interval
# High = highest price in n minute interval
# Low = lowest price in n min interval
# Close = close of the last minute in n minute interval
# Volume = sum of volume for each minute in n minute interval


def convert(timeframes, dataset=data):
    '''
    Convert selected dataset to specified time frames.
    
    timeframes: list of desired timeframes in minutes format
    dataset: dataset to be converted
    
    Example:
    timeframes = [5,10,15]    
    dataset = data
    '''
    
    ohlc_dict = {                                                                                                             
            'Open': 'first',                                                                                                    
            'High': 'max',                                                                                                       
            'Low': 'min',                                                                                                        
            'Close': 'last',                                                                                                    
            'Volume': 'sum'
            }

    for i in timeframes:
        dataset.resample(str(i)+"T", how=ohlc_dict, closed='left', label='left').to_csv(exchange + "_" + pair + "_" + str(i) + "m.csv")
        
    
    return str(len(timeframes)) + " files created."


convert([5,10,15,30,60,120,240], dataset=data)
