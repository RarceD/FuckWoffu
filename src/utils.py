import json
import time
import logging
from datetime import datetime, timedelta
from src.SignInWoffu import *
from src.Telegram import notify

def get_json_data():
    with open('config/secrets.json', 'r') as file:
        json_content = json.load(file)
        return json_content['email'], json_content['password'], json_content['companyName'], json_content['times'], json_content['lunch_times'], json_content['summer_times'], json_content['summer_period'], json_content['unpunctuality']


def is_sign_hour(signTimes, delay) -> bool:
    current_time = time.strftime("%H:%M") - timedelta(delay)
    weekday = time.localtime(time.time()).tm_wday
    return current_time in signTimes and weekday not in {5, 6}


def is_lunch_time(lunch_sign_times) -> bool:
    current_time = time.strftime("%H:%M")
    weekday = time.localtime(time.time()).tm_wday
    return current_time in lunch_sign_times and weekday not in {5, 6}


def is_end_of_day(times, delay) -> bool:
    current_time = time.strftime("%H:%M") - timedelta(delay)
    return current_time == times[-1]


def is_holidays(holidays) -> bool:
    current_time = datetime.today()
    return any(pto.month == current_time.month and pto.day == current_time.day and pto.year == current_time.year 
               for pto in holidays)


def is_summer_time(summer_period) -> bool:
    current_time = datetime.today()
    return (current_time.day >= summer_period[0].day and current_time.day <= summer_period[1].day 
            and current_time.month >= summer_period[0].month and current_time.day <= summer_period[1].month)


def sign_in(sign_in_app: SignInWoffu):
    holidays = sign_in_app.get_holiday()
    if not is_holidays(holidays):
        success = sign_in_app.sign_in()
        if success:
            notify('Sign in/out succesfully')
            logging.info('Sign in succesfully')
        else:
            logging.error('Error maybe something should be done  ¯\(ツ)/¯ ')
    else:
        logging.info('I am on holiday, no check in')