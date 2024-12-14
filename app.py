from flask import Flask
import telegram_notification as tele
import util
import history_service as hs
import json
import trading_view_service as tvs
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__)
scheduler = BackgroundScheduler()

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

@app.route('/get/history')
def get_history_nifty_atm_ce():
    nifty_atm_call = json.loads(util.get_nifty_atm_ce())
    print(nifty_atm_call)
    exchange = nifty_atm_call['exchange']
    symbol_token = nifty_atm_call['token']
    interval = 'FIVE_MINUTE'
    from_date = '2022-12-14 09:16'
    to_date = '2024-12-14 09:16'
    his = hs.get_historical_data(exchange, symbol_token, interval, from_date, to_date)
    his = tvs.get_sma_22_and_adx_8(his)
    return his.tail(20).values.tolist()


def my_cron_job():
    print('Inside schedulers!')
    send_message('Test schedulers!')

scheduler.add_job(
    func=my_cron_job,
    trigger=CronTrigger(hour=19, minute=52, timezone='Asia/Kolkata'),
)

# Start the scheduler
scheduler.start()


# Befor pushing to git please comment the below 2 lines
# if __name__ == '__main__':
#     app.run()