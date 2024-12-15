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

app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello World!'

def ncb_job():
    try:
        logger.info(f"ncb_job executed at {datetime.now()}")
        india_tz = util.time_zone_ist()
        # Get the current time in UTC and convert it to IST
        now = datetime.now(pytz.utc).astimezone(india_tz)

        start_time = now.replace(hour=9, minute=20, second=0, microsecond=0)
        end_time = now.replace(hour=13, minute=30, second=0, microsecond=0)

        if (now > start_time) and (now < end_time):
            ncb.buy_ce()
        else:
            logger.info(
                f"Current time {now.strftime('%H:%M:%S')} is before 09:20 PM IST OR after 13:30 PM IST. Exiting method.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")

# Initialize the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule job to run every 5 seconds
    scheduler.add_job(ncb_job, IntervalTrigger(seconds=10))
    scheduler.start()
    print("Scheduler started.")

start_scheduler()


# Befor pushing to git please comment the below 2 lines
# if __name__ == '__main__':
#     app.run(use_reloader=False)