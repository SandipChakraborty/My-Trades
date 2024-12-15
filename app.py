import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
import time
from datetime import datetime, timedelta
from flask import Flask
import nifty_call_buy as ncb
import telegram_notification as tele
import util
import pytz
from logzero import logger
import cron_jobs as jobs

app = Flask(__name__)

@app.route('/')
def test():
    res = tt()
    res = json.loads(res)
    res['token'] = 'token_num'
    if res['punch_order']:
        logger.info('punch order')
        tele.callBot(res)
    else:
        logger.info('No order placed!')
    return 'Hello World!'

def tt():
    value = {
            "punch_order": True,
            "buy_price": 51,
            "sl": 10,
            "target": 20
        }
    return json.dumps(value)

# Initialize the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule job to run every 5 seconds
    scheduler.add_job(jobs.ncb_job, IntervalTrigger(seconds=10))
    scheduler.add_job(jobs.npb_job, IntervalTrigger(seconds=10))
    scheduler.start()
    logger.info("Scheduler started.")

start_scheduler()


# Before pushing to git please comment the below 2 lines
# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=False)