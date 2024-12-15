import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask
import telegram_notification as tele
import util
import nifty_call_buy as ncb

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/')
def test():
    return 'Hello World!'

@app.route('/send_telegram_msg/<string:msg>')
def send_message(msg: str):
    return tele.callBot(msg)



def my_cron_job():
    send_message('Test schedulers!')

scheduler.add_job(
    func=my_cron_job,
    trigger=CronTrigger(hour=9, minute=15, timezone=util.time_zone_ist()),
)

# Start the scheduler
scheduler.start()


# Befor pushing to git please comment the below 2 lines
if __name__ == '__main__':
    app.run()