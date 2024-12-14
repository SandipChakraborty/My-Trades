from tvDatafeed import TvDatafeed, Interval

# Importing the pandas library
# and giving it an alias 'pd'
import pandas as pd

# Importing the pandas_ta library
# and giving it an alias 'ta'
import pandas_ta as ta

def get_sma_22_and_adx_8(df):
    df["adx"] = ta.adx(df['high'], df['low'], df['close'], 8)['ADX_8']
    df["sma_22"] = ta.sma(df['close'], 22)
    return df







