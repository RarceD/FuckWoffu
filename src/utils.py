import json
import logging
from datetime import datetime, timedelta
from random import randrange
from src.SignInWoffu import *

def get_json_data():
    with open("config/config.json", "r") as file:
        json_content = json.load(file)
        return (
            json_content["email"],
            json_content["password"],
            json_content["companyName"],
            json_content["times"],
            json_content["summer_times"],
            json_content["summer_period"],
            json_content["unpunctuality"],
            json_content["lunch_unpunctuality"],
            json_content["lunch_time"],
            json_content["min_time_to_lunch"],
            json_content["max_time_to_lunch"],
        )


def is_sign_hour(sign_times, delay) -> bool:
    current_time = (datetime.now() - timedelta(minutes=delay)).strftime("%H:%M")

    is_sign_hour = current_time in sign_times
    if is_sign_hour:
        logging.info("Signing in/out time!")
    return is_sign_hour


def is_lunch_time(lunch_sign_times, lunch_delay) -> bool:
    current_time = (datetime.now() - timedelta(minutes=lunch_delay)).strftime("%H:%M")

    is_lunch_time = current_time in lunch_sign_times
    if is_lunch_time:
        if current_time == lunch_sign_times[0]:
            logging.info("Lunch time!")
        else:
            logging.info("Back from lunch!")
    return is_lunch_time


def is_end_of_day(times, delay) -> bool:
    current_time = (datetime.now() - timedelta(minutes=delay)).strftime("%H:%M")
    return current_time == times[-1]


def is_working_day(holidays) -> bool:
    current_time = datetime.today()
    is_holidays = any(
        pto.month == current_time.month
        and pto.day == current_time.day
        and pto.year == current_time.year
        for pto in holidays
    )
    if is_holidays:
        logging.info("Today is a holiday!")

    weekday = current_time.weekday()
    is_weekend = weekday in {5, 6}
    if is_weekend:
        logging.info("Today is weekend!")

    return not (is_holidays or is_weekend)


def is_summer_time(summer_period) -> bool:
    if summer_period is None:
        return False
    current_time = datetime.today()
    return summer_period[0] <= current_time <= summer_period[1]


def set_lunch_times(lunch_time, min_time_to_lunch, max_time_to_lunch):
    if lunch_time is None:
        return []

    lunch_start = datetime.strptime(lunch_time, "%H:%M")
    lunch_duration = randrange(min_time_to_lunch, max_time_to_lunch)
    lunch_end = lunch_start + timedelta(minutes=lunch_duration)

    return [lunch_start.strftime("%H:%M"), lunch_end.strftime("%H:%M")]


def fix_times_format(times):
    return [datetime.strptime(time, "%H:%M").strftime("%H:%M") for time in times]


def sign_in(sign_in_app: SignInWoffu):
    holidays = sign_in_app.get_holiday()
    if is_working_day(holidays):
        sign_in_app.sign_in()
    else:
        logging.info("No work day, no check in")
