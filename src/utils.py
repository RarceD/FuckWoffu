import json
import logging
from datetime import datetime, timedelta
from random import randrange
from src.SignInWoffu import *

def get_json_data():
    with open("config/config.json", "r") as file:
        json_content = json.load(file)

        # Email
        if json_content["email"] == "":
            logging.error("Email is empty. Stopping")
            raise ValueError("Email is empty")

        # Password
        if json_content["password"] == "":
            logging.error("Password is empty. Stopping")
            raise ValueError("Password is empty")

        # Company name
        if json_content["companyName"] == "":
            logging.error("Company name is empty. Stopping")
            raise ValueError("Company name is empty")

        # Times
        if json_content["times"] == []:
            if json_content["summer_period"] == []:
                logging.error("Times are empty. Stopping")
                raise ValueError("Times are empty")
            else:
                if json_content["summer_times"] != []:
                    logging.warning("Times are empty, but summer period is set")
                else:
                    logging.error("Times are empty. Stopping")
                    raise ValueError("Times are empty")

        elif len(json_content["times"]) % 2 != 0:
            logging.error("Times are not even. Stopping")
            raise ValueError("Times are not even")

        # Summer period and summer times
        if json_content["summer_period"] == []:
            json_content["summer_period"] = None

        if (
            json_content["summer_period"] is not None
            and json_content["summer_times"] == []
        ):
            logging.warning("Summer period is set but summer times are empty")

        # Lunch times
        if json_content["lunch_time"] == "":
            json_content["lunch_time"] = None

        # Max time to lunch
        if (
            json_content["lunch_time"] is not None
            and json_content["max_time_to_lunch"] == ""
        ):
            logging.warning("Lunch time is set but max time to lunch is empty")
            json_content["max_time_to_lunch"] = 0

        elif (
            json_content["lunch_time"] is not None
            and json_content["max_time_to_lunch"] == 0
        ):
            logging.warning("Max time to lunch is 0")

        elif (
            json_content["lunch_time"] is not None
            and json_content["max_time_to_lunch"] < 0
        ):
            logging.warning("Max time to lunch is negative. Stopping")
            raise ValueError("Max time to lunch is negative")

        # Min time to lunch
        if (
            json_content["lunch_time"] is not None
            and json_content["min_time_to_lunch"] == ""
        ):
            logging.warning("Min time to lunch is empty. Setting it to 0")
            json_content["min_time_to_lunch"] = 1

        elif (
            json_content["lunch_time"] is not None
            and json_content["min_time_to_lunch"] < 1
        ):
            logging.error("Min time to lunch can't be less than 1. Stopping")
            raise ValueError("Min time to lunch can't be less than 1")

        # Both
        elif json_content["min_time_to_lunch"] > json_content["max_time_to_lunch"]:
            logging.warning(
                "Min time to lunch is greater than max time to lunch, switching values"
            )
            json_content["min_time_to_lunch"], json_content["max_time_to_lunch"] = (
                json_content["max_time_to_lunch"],
                json_content["min_time_to_lunch"],
            )

        # Unpunctuality
        if json_content["unpunctuality"] < 0:
            logging.error("Unpunctuality is negative. Stopping")
            raise ValueError("Unpunctuality is negative")

        if json_content["lunch_unpunctuality"] < 0:
            logging.error("Lunch unpunctuality is negative. Stopping")
            raise ValueError("Lunch unpunctuality is negative")

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
    current_time = (datetime.today() - timedelta(minutes=delay)).strftime("%H:%M")

    is_sign_hour = current_time in sign_times
    if is_sign_hour:
        if current_time == sign_times[0]:
            logging.info("Time to start!")
    return is_sign_hour


def is_lunch_time(lunch_sign_times, lunch_delay) -> bool:
    current_time = (datetime.today() - timedelta(minutes=lunch_delay)).strftime("%H:%M")

    is_lunch_time = current_time in lunch_sign_times
    if is_lunch_time:
        if current_time == lunch_sign_times[0]:
            logging.info("Lunch time!")
        else:
            logging.info("Back from lunch!")
    return is_lunch_time


def is_end_of_day(times, delay) -> bool:
    current_time = (datetime.today() - timedelta(minutes=delay)).strftime("%H:%M")
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

    if max_time_to_lunch == 0:
        logging.error("Max time to lunch is 0. Stopping")
        raise ValueError("Max time to lunch is 0")
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
