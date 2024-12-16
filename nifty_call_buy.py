from logzero import logger
import history_service as hs
import json
import util
import trading_view_service as tvs
import telegram_notification as tele
from datetime import datetime, timedelta
import candle as cdl

ce_buy_order_status: json = None

def get_latest_chart(exchange, symbol_token, interval, from_date, to_date):
    his = hs.get_historical_data(exchange, symbol_token, interval, from_date, to_date)
    his = tvs.get_sma_22_and_adx_8(his)
    return his


def buy_ce():
    # logger.info('nifty call buy started')
    nifty_atm_call = json.loads(util.get_nifty_atm_ce())
    # logger.info(nifty_atm_call)
    exchange = nifty_atm_call['exchange']
    symbol_token = nifty_atm_call['token']
    interval = 'FIVE_MINUTE'
    while True:
        now = datetime.now(util.time_zone_ist())
        one_day_back = datetime.today() - timedelta(days=1)
        # from_date and to_date pattern '2022-12-14 09:16'
        from_date = one_day_back.strftime("%Y-%m-%d") + " 13:00"
        to_date = now.strftime("%Y-%m-%d") + " 13:00"
        df = get_latest_chart(exchange, symbol_token, interval, from_date, to_date)
        res = json.loads(analise_df(df))
        # res structure
        #         value = {
        #         "punch_order": False,
        #         "buy_price": 0,
        #         "sl": 0,
        #         "target": 0
        #     }
        if res['punch_order']:
            logger.info('punch order')
            res['exchange'] = exchange
            res['symbol_token'] = symbol_token
            tele.callBot(res)
        else:
            logger.info('No order placed!')


def is_having_inclining_sma_22(data, window=5) -> bool:
    sma_incline = []
    for i in range(1, len(data)):
        if data['sma_22'][i] >= data['sma_22'][i - 1]:
            sma_incline.append(True)
        else:
            sma_incline.append(False)
    sma_incline.insert(0, False)
    data['sma_22_incline'] = sma_incline
    last_n_rows = data['sma_22_incline'].tail(window).tolist()
    for item in last_n_rows:
        if item is False:
            return False
    return True


def is_last_candle_took_support_on_sma_22(df, window=22, tolerance=0.001) -> bool:
    support_detected = []
    for i in range(len(df)):
        if i >= window - 1:
            sma_value = df['sma_22'][i]
            low_price = df['low'][i]
            if sma_value * (1 - tolerance) <= low_price <= sma_value * (1 + tolerance):
                support_detected.append(True)
            else:
                support_detected.append(False)
        else:
            support_detected.append(False)

    df['support_on_sma_22'] = support_detected
    return df.tail(1)['support_on_sma_22'].values(0)

def is_last_candle_bullish(df) -> bool:
    cdf = df.tail(1)
    o = cdf['open'].values(0)
    h = cdf['high'].values(0)
    l = cdf['low'].values(0)
    c = cdf['close'].values(0)
    if cdl.is_hammer(o, h, l, c):
        return True
    if cdl.is_green(o, c) & cdl.is_marubozu(o, h, l, c):
        return True
    return False

def is_adx_greater_than_20(df) -> bool:
    if df.tail(1)['adx'].values(0) >= 20:
        return True
    return False


def analise_df(df) -> json:
    value = {
        "punch_order": False,
        "buy_price": 0,
        "sl": 0,
        "target": 0
    }
    if not is_having_inclining_sma_22(df, window=5):
        return json.dumps(value)
    if not is_last_candle_took_support_on_sma_22(df):
        return json.dumps(value)
    if not is_last_candle_bullish(df):
        return json.dumps(value)
    if not is_adx_greater_than_20(df):
        return json.dumps(value)

    cdf = df.tail(1)
    o = cdf['open'].values(0)
    h = cdf['high'].values(0)
    l = cdf['low'].values(0)
    c = cdf['close'].values(0)
    buy_price = (h+2)
    sl = (h-l+1)
    target = sl * 2

    # Calculate the value json
    value = {
        "punch_order": True,
        "buy_price": buy_price,
        "sl": sl,
        "target": target
    }
    return json.dumps(value)
