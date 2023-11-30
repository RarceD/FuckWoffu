import sched
import time
import logging
from Telegram import notify
from src.SignInWoffu import *
from src.utils import *

logging.basicConfig(
    filename='logs/fuckWoffu.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

'''
    Every 60 seconds I check my enter/leave time and execute request
'''
TIME_TO_CHECK = 60


def main(scheduler):
    email, password, sign_times, company_name = get_json_data()
    if is_sign_hour(sign_times):
        sign_in_app = SignInWoffu(email, password, company_name)
        holidays = sign_in_app.get_holiday()
        if not is_holidays(holidays):
            success = sign_in_app.sign_in()
            if success:
                notify('Sign in/out succesfully')
                logging.warning('Sign in succesfully')
            else:
                logging.error('Error maybe something should be done  ¯\(ツ)/¯ ')
        else:
            logging.warning('I am on holiday, no check in')

    # Restart the timer
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))


if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))
    scheduler.run()
