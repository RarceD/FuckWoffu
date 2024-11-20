import argparse
import sched
import time
import logging
from src.Telegram import notify
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
ERROR_MESSAGE = 'Error maybe something should be done  ¯\(ツ)/¯ '
SO_FAR_SO_GOOD_MESSAGE = 'So far, so good!'
ERROR_TOKEN = '¯\(ツ)/¯'

def main(scheduler):
    email, password, sign_times, company_name = get_json_data()
    if True:
        sign_in_app = SignInWoffu(email, password, company_name)
        holidays = sign_in_app.get_holiday()
        if not is_holidays(holidays):
            success = sign_in_app.sign_in()
            if success:
                notify('Sign in/out succesfully')
                logging.warning('Sign in succesfully')
            else:
                logging.error()
        else:
            logging.warning('I am on holiday, no check in')

    # Restart the timer
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))

def testConection():
    email, password, sign_times, company_name = get_json_data()
    try:
        sign_in_app = SignInWoffu(email, password, company_name)
        if sign_in_app.token == ERROR_TOKEN:
            logging.error(ERROR_MESSAGE)
            print(ERROR_MESSAGE)
        else:
            logging.info(SO_FAR_SO_GOOD_MESSAGE)
            print(SO_FAR_SO_GOOD_MESSAGE)
    except Exception as e:
        message = f'An error occurred during sign-in: {e}'
        logging.error(message)
        print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Woffu Auto Check-In script') 
    parser.add_argument('--test', help='Optional test parameter', action='store_true') 
    args = parser.parse_args()

    if args.test:
        testConection()
    else: 
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))
        scheduler.run()
