import os
from SmartApi import SmartConnect
from logzero import logger
import pyotp
import requests
import pandas as pd
import json
from datetime import datetime
import math

def set_env_var(name='SANDIP', value='CHAKRABORTY'):
    os.environ[name] = value
    return os.environ.get(name)

def get_env_var(var_name):
    return os.environ.get(var_name, "not_found")

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def get_angel_api_key():
    return get_env_var('trading_api_key')

def get_angel_user():
    return get_env_var('angel_user')

def get_angel_pwd():
    return get_env_var('angel_pwd')

def get_angel_qr_code():
    return get_env_var('my_qr_code')

def get_session():
    obj=SmartConnect(api_key=get_angel_api_key())
    totp = pyotp.TOTP(get_angel_qr_code())
    totp = totp.now()

    data = obj.generateSession(get_angel_user(), get_angel_pwd(), totp=totp)

    refresh_token= data['data']['refreshToken']

    #fetch the feed_token
    feed_token=obj.getfeedToken()

    #fetch User Profile
    # user_profile= obj.getProfile(refresh_token)
    # print(user_profile)
    return obj

def get_ltp(exchange, symbol, token):
    session = get_session()
    print('token - ', token)
    return session.ltpData(exchange, symbol, token)

def log_out():
    try:
        session = SmartConnect(api_key=get_angel_api_key())
        SmartConnect.terminateSession(session,clientCode=get_angel_user())
        logger.info("Logout Successful")
    except Exception as e:
        logger.exception(f"Logout failed: {e}")

def get_master_list():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    df = pd.DataFrame.from_dict(d)
    df = df.astype({'strike': float})
    return df

def get_maruti_current_expiry_fut():
    df = get_master_list()
    df = df[df['exch_seg'] == 'NFO']
    df = df[df['name'] == 'MARUTI']
    df = df[df['instrumenttype'] == 'FUTSTK']
    expiry_column = df['expiry']
    new_expiry_column = expiry_column.apply(convert_date)
    df['expiry'] = new_expiry_column
    df = df.sort_values("expiry")
    df = df.head(1)
    return convert_order_details(df)

def get_bank_nifty_current_expiry_fut():
    df = get_master_list()
    df = df[df['exch_seg'] == 'NFO']
    df = df[df['name'] == 'BANKNIFTY']
    df = df[df['instrumenttype'] == 'FUTIDX']
    expiry_column = df['expiry']
    new_expiry_column = expiry_column.apply(convert_date)
    df['expiry'] = new_expiry_column
    df = df.sort_values("expiry")
    df = df.head(1)
    return convert_order_details(df)

def get_nifty_ltp(master_list_df):
    return get_idx_ltp(master_list_df)

def get_bank_nifty_ltp(master_list_df):
    return get_idx_ltp(master_list_df, symbol='BANKNIFTY', name='BANKNIFTY')

def get_idx_ltp(df_ltp, exg='NSE', symbol='NIFTY', name='NIFTY'):
    df_ltp = df_ltp[df_ltp['exch_seg'] == exg]
    df_ltp = df_ltp[df_ltp['symbol'] == symbol]
    df_ltp = df_ltp[df_ltp['name'] == name]
    nifty_ltp = get_ltp(exg, symbol, df_ltp['token'].head(1).values[0])
    return nifty_ltp['data']['ltp']

def get_nifty_atm_ce():
    df = get_master_list()
    nifty_ltp = get_nifty_ltp(df)
    ce_atm_strike = roundup(nifty_ltp)
    df = df[df['exch_seg'] == 'NFO']
    df = df[df['name'] == 'NIFTY']
    df = df[df['instrumenttype'] == 'OPTIDX']
    expiry_column = df['expiry']
    new_expiry_column = expiry_column.apply(convert_date)
    df['expiry_date'] = new_expiry_column
    df = df.sort_values("expiry_date")
    exp_value = df.head(1)['expiry'].values[0][:5] + df.head(1)['expiry'].values[0][-4:][-2:]
    symbol = df.head(1)['name'].values[0] + exp_value + str(ce_atm_strike) + 'CE'
    df = df[df['symbol'] == symbol]
    df = df.head(1)
    return convert_order_details(df)

def get_nifty_atm_pe():
    df = get_master_list()
    nifty_ltp = get_nifty_ltp(df)
    pe_atm_strike = roundup(nifty_ltp)-100
    df = df[df['exch_seg'] == 'NFO']
    df = df[df['name'] == 'NIFTY']
    df = df[df['instrumenttype'] == 'OPTIDX']
    expiry_column = df['expiry']
    new_expiry_column = expiry_column.apply(convert_date)
    df['expiry_date'] = new_expiry_column
    df = df.sort_values("expiry_date")
    exp_value = df.head(1)['expiry'].values[0][:5] + df.head(1)['expiry'].values[0][-4:][-2:]
    symbol = df.head(1)['name'].values[0] + exp_value + str(pe_atm_strike) + 'PE'
    df = df[df['symbol'] == symbol]
    df = df.head(1)
    return convert_order_details(df)

def convert_date(date_time_str: str):
    datetime_obj = datetime.strptime(date_time_str, "%d%b%Y")
    return datetime_obj

def convert_order_details(df):
    exchange = df['exch_seg'].values[0]
    token = df['token'].values[0]
    symbol = df['symbol'].values[0]
    name = df['name'].values[0]
    expiry = df['expiry'].values[0]
    lotsize = df['lotsize'].values[0]
    value = {
        "exchange": exchange,
        "token": token,
        "symbol": symbol,
        "name": name,
        "lotsize": lotsize,
        "expiry": str(expiry)
    }
    return json.dumps(value)
