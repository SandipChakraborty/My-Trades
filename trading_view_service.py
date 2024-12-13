from tvDatafeed import TvDatafeed, Interval

import talib

def test():
    tv = TvDatafeed()

    df = tv.get_hist(symbol='TATAPOWER', exchange="NSE", interval=Interval.in_5_minute, n_bars=1000,
                     extended_session=False)
    df = df.reset_index()

    df["adx"] = talib.ADX(df['high'], df['low'], df['close'], 8)

    df["plus_di"] = talib.PLUS_DI(df['high'], df['low'], df['close'], 8)
    df["minus_di"] = talib.MINUS_DI(df['high'], df['low'], df['close'], 8)

    df["sma_22"] = talib.SMA(df['close'], 8)
    df["ema_22"] = talib.EMA(df['close'], 8)

    print(df.tail(500))







