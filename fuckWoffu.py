import json
import sched
import time
from datetime import datetime
import logging

from SignInWoffu import SignInWoffu

logging.basicConfig(
    filename='logs/fuckWoffu.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

def get_json_data():
    with open('secrets.json', 'r') as file:
        json_content = json.load(file)
        return json_content['email'], json_content['password'], json_content['times'], json_content['companyName']


def is_sign_hour(signTimes) -> bool:
    current_time = time.strftime("%H:%M")
    weekday = time.localtime(time.time()).tm_wday
    return current_time in signTimes and weekday not in {5, 6}


def is_holidays(holidays) -> bool:
    current_time = datetime.today()
    return any(pto.month == current_time.month and pto.day == current_time.day for pto in holidays)


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
                logging.warning('Sign in succesfully')
            else:
                logging.error('Error maybe something should be done  ¯\(ツ)/¯ ')

    # Restart the timer
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))


if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))
    scheduler.run()
