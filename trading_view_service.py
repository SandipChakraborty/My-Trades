from tvDatafeed import TvDatafeed, Interval
import pandas_ta as ta


def test():
    tv = TvDatafeed()

    df = tv.get_hist(symbol='TATAPOWER', exchange="NSE", interval=Interval.in_5_minute, n_bars=1000,
                     extended_session=False)
    df = df.reset_index()
    #
    df["adx"] = ta.adx(df['high'], df['low'], df['close'], 8)
    #
    # df["sma_22"] = pandas_ta.sma(df['close'], 8)
    # df["ema_22"] = pandas_ta.ema(df['close'], 8)

    print(df.tail(500))







