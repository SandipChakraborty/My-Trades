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
def home():
    return 'Hello World!'

@app.route('/msg/<string:text>')
def tele_msg(text):
    return tele.callBot(text)

# Initialize the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule job to run every 10 seconds
    scheduler.add_job(jobs.ncb_job, IntervalTrigger(seconds=10))
    scheduler.add_job(jobs.npb_job, IntervalTrigger(seconds=10))
    scheduler.start()
    logger.info("Scheduler started.")

start_scheduler()


# Before pushing to git please comment the below 2 lines
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)