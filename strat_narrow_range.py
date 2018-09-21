import pandas as pd

df_60m = pd.read_csv('gemini_BTCUSD_60m.csv')
df_1m = pd.read_csv('gemini_BTCUSD_1min.csv')

df_60m['Returns'] = df_60m['Close'].pct_change()
df_1m['Returns'] = df_1m['Close'].pct_change()

df_60m['High_Low_Range'] = df_60m['High'] - df_60m['Low']
df_1m['High_Low_Range'] = df_1m['High'] - df_1m['Low']

df_60m['Lowest_Range_4_Period'] = df_60m['High_Low_Range'].rolling(4, min_periods=4).min()
df_60m['Lowest_Range_7_Period'] = df_60m['High_Low_Range'].rolling(7, min_periods=7).min()

df_1m['Lowest_Range_4_Period'] = df_1m['High_Low_Range'].rolling(4, min_periods=4).min()
df_1m['Lowest_Range_7_Period'] = df_1m['High_Low_Range'].rolling(7, min_periods=7).min()

print(df_60m.head(20))

print(df_1m.head(20))