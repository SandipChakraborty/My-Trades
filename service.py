import login as l
import pyotp
import pandas as pd
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect

#import smartapi.smartExceptions(for smartExceptions)

#create object of call
# history_obj=SmartConnect(api_key=l.history_api_key)

# totp = pyotp.TOTP(l.my_qr_code)
# totp = totp.now()

# data = obj.generateSession(l.angel_user, l.angel_pwd, totp=totp)

# refreshToken= data['data']['refreshToken']

# #fetch the feedtoken
# feedToken=obj.getfeedToken()

# #fetch User Profile
# userProfile= obj.getProfile(refreshToken)
# print(userProfile)

def fetchHistoryObjectToCallHistorycalData():
    history_obj=SmartConnect(api_key=l.history_api_key)
    totp = pyotp.TOTP(l.my_qr_code)
    totp = totp.now()

    data = history_obj.generateSession(l.angel_user, l.angel_pwd, totp=totp)

    refreshToken= data['data']['refreshToken']

    #fetch the feedtoken
    feedToken=history_obj.getfeedToken()

    #fetch User Profile
    userProfile= history_obj.getProfile(refreshToken)
    # print(userProfile)
    return history_obj


def getHistoryCalData(exchange, symboltoken, interval, fromdate, todate):
    #Historic api
    try:
        obj = fetchHistoryObjectToCallHistorycalData()
        historicParam={
        "exchange": exchange,
        "symboltoken": symboltoken,
        "interval": interval,
        "fromdate": fromdate, 
        "todate": todate
        }
        history_data = obj.getCandleData(historicParam)['data']
        history = pd.DataFrame(history_data)
        history = history.rename(columns={0: "datetime", 1: "open", 2: "high", 3: "low", 4: "close", 5: "volume"})
        history['datetime'] = pd.to_datetime(history['datetime'])
        history = history.set_index('datetime')
        print(history)
        return history_data
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))





