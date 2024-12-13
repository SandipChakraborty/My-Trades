from tvDatafeed import TvDatafeed, Interval

# Importing the pandas library
# and giving it an alias 'pd'
import pandas as pd

# Importing the pandas_ta library
# and giving it an alias 'ta'
import pandas_ta as ta



def test():

    tv = TvDatafeed()
    # df = pd.DataFrame()
    df = tv.get_hist(symbol='TATAPOWER', exchange="NSE", interval=Interval.in_5_minute, n_bars=1000,
                     extended_session=False)
    df = df.reset_index()

    #
    df["adx"] = ta.adx(df['high'], df['low'], df['close'], 8)['ADX_8']
    #
    df["sma_22"] = ta.sma(df['close'], 8)
    # df["ema_22"] = pandas_ta.ema(df['close'], 8)

    print(df.tail(5))
    return df.tail(50)







