import requests
import pandas as pd
import numpy as np

# Define function to calculate Super Trend
def super_trend(df, atr_period=7, multiplier=3):
    """
    Function to calculate Super Trend indicator for given Dataframe
    """
    df['ATR'] = df['high'] - df['low']
    df['ATR'] = df['ATR'].rolling(atr_period).mean()
    df['Upper Basic'] = (df['high'] + df['low']) / 2 + multiplier * df['ATR']
    df['Lower Basic'] = (df['high'] + df['low']) / 2 - multiplier * df['ATR']
    df['Upper Band'] = df['Upper Basic']
    df['Lower Band'] = df['Lower Basic']
    for i in range(atr_period, len(df)):
        if df['close'][i - 1] > df['Upper Band'][i - 1]:
            df['Upper Band'][i] = df['Lower Basic'][i]
        else:
            df['Upper Band'][i] = df['Upper Basic'][i]
        if df['close'][i - 1] < df['Lower Band'][i - 1]:
            df['Lower Band'][i] = df['Upper Basic'][i]
        else:
            df['Lower Band'][i] = df['Lower Basic'][i]
    df['SuperTrend'] = np.nan
    for i in range(atr_period, len(df)):
        if df['close'][i] <= df['Upper Band'][i]:
            df['SuperTrend'][i] = df['Upper Band'][i]
        elif df['close'][i] > df['Upper Band'][i]:
            df['SuperTrend'][i] = df['Lower Band'][i]
    return df

# Make API request to get market data
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
response = requests.get(url)

# Parse JSON response to Dataframe
data = response.json()['Time Series (5min)']
df = pd.DataFrame(data).T
df.index = pd.to_datetime(df.index)
df = df.astype(float)
df.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'}, inplace=True)

# Apply Super Trend indicator
df = super_trend(df)

# Display results
print(df.tail())
