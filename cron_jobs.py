from datetime import datetime, timedelta
import nifty_call_buy as ncb
import nifty_put_buy as npb
import util
import pytz
from logzero import logger


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
            logger.debug(
                f"Current time {now.strftime('%H:%M:%S')} is before 09:20 PM IST OR after 13:30 PM IST. Exiting method.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")

def npb_job():
    try:
        logger.info(f"npb_job executed at {datetime.now()}")
        india_tz = util.time_zone_ist()
        # Get the current time in UTC and convert it to IST
        now = datetime.now(pytz.utc).astimezone(india_tz)

        start_time = now.replace(hour=9, minute=20, second=0, microsecond=0)
        end_time = now.replace(hour=13, minute=30, second=0, microsecond=0)

        if (now > start_time) and (now < end_time):
            npb.buy_pe()
        else:
            logger.debug(
                f"Current time {now.strftime('%H:%M:%S')} is before 09:20 PM IST OR after 13:30 PM IST. Exiting method.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
