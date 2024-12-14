import util
import pandas as pd

from util import log_out


def get_historical_data(exchange, symbol_token, interval, from_date, to_date):
    obj = util.get_session()
    try:
        historic_param={
        "exchange": exchange,
        "symboltoken": symbol_token,
        "interval": interval,
        "fromdate": from_date,
        "todate": to_date
        }
        history_data = obj.getCandleData(historic_param)['data']
        # print(history_data)
        history = pd.DataFrame(history_data)
        history = history.rename(columns={0: "datetime", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"})
        # history['datetime'] = pd.to_datetime(history['datetime'])
        # history = history.set_index('datetime')
        # print(history)
        log_out()
        return history
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))





