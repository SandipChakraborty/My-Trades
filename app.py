import asyncio
from flask import Flask
import telegram_notification as tele
import util
import async_service
import threading
import trading_view_service as tv

app = Flask(__name__)

@app.route('/')
def test():
    return "Hello Sandip!"

# @app.route('/test_script')
# def run_script():
#     t1 = threading.Thread(target=asyncio.run(async_service.run_script()))
#     t1.start()
#     print("Done!")
#     return "Script triggered"

@app.route('/send_telegram_msg/<string:msg>')
def send_message(msg: str):
    return tele.callBot(msg)

@app.route('/maruti')
def maruti():
    res = util.get_maruti_current_expiry_fut()
    return res

@app.route('/bank_nifty')
def bank_nifty():
    res = util.get_bank_nifty_current_expiry_fut()
    return res

@app.route('/nifty/atm/ce')
def nifty_atm_ce():
    res = util.get_nifty_atm_ce()
    print(res)
    return res

@app.route('/nifty/atm/pe')
def nifty_atm_pe():
    res = util.get_nifty_atm_pe()
    print(res)
    return res

@app.route('/ta_lib')
def ta_lib():
    try:
        tv.test()
        return "Success"
    except Exception as e:
        print("Historic Api failed: {}".format(e))
        return "Failure"

# @app.route('/set/env/<string:name>/<string:val>')
# def set_env_var(name, val):
#     sensitive_env_var = ['trading_api_key', 'angel_user', 'angel_pwd', 'my_qr_code']
#     if name in sensitive_env_var:
#         return "Its sensitive!"
#     res = util.set_env_var(name, val)
#     return res
#
# @app.route('/get/env/<string:name>')
# def get_env_var(name):
#     sensitive_env_var = ['trading_api_key', 'angel_user', 'angel_pwd', 'my_qr_code']
#     if name in sensitive_env_var:
#         return "Its sensitive!"
#     res = util.get_env_var(name)
#     return res

# Befor pushing to git please comment the below 2 lines
if __name__ == '__main__':
    app.run()