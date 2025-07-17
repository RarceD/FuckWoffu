import sched
import time
import logging
import argparse
import os
from random import randrange
from src.utils import *


def conf_logging(loglevel):
    # Create log file if it does not exist
    log_dir = os.path.dirname("logs/fuckWoffu.log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename="logs/fuckWoffu.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=loglevel.upper(),
    )


'''
    Every 60 seconds I check my enter/leave time and execute request
'''
TIME_TO_CHECK = 60
delay = None
lunch_delay = None
lunch_times = None


def main(scheduler, delay, lunch_delay, lunch_times):
    (
        email,
        password,
        company_name,
        times,
        summer_times,
        summer_period,
        unpunctuality,
        lunch_unpunctuality,
        lunch_time,
        min_time_to_lunch,
        max_time_to_lunch,
    ) = get_json_data()

    # Setting up delays, times and dates for the first time
    if delay is None:
        logging.info("Setting up delays and times for the first time")
        delay = randrange(unpunctuality) if unpunctuality > 0 else 0
    if lunch_delay is None:
        lunch_delay = randrange(lunch_unpunctuality) if lunch_unpunctuality > 0 else 0
    if lunch_times is None:
        lunch_times = set_lunch_times(lunch_time, min_time_to_lunch, max_time_to_lunch)
    summer = (
        None
        if summer_period is None
        else [
            datetime.strptime(f"{date}/{datetime.today().year}", "%d/%m/%Y")
            for date in summer_period
        ]
    )
    times = fix_times_format(times)
    summer_times = fix_times_format(summer_times)

    if is_summer_time(summer):  # Summer time
        if is_sign_hour(summer_times, delay):
            if is_end_of_day(summer_times, delay):
                time.sleep(randrange(unpunctuality) * 60)  # Randomizing time to leave
                logging.info("End of day!")
                sign_in(email, password, company_name)

                delay = randrange(unpunctuality)  # Create new random delay for next day

                time.sleep(unpunctuality * 60)
            else:
                sign_in(email, password, company_name)

    else:  # Regular time
        if is_sign_hour(times, delay) or is_lunch_time(lunch_times, lunch_delay):
            if is_end_of_day(times, delay):
                time.sleep(randrange(unpunctuality) * 60)  # Randomizing time to leave
                logging.info("End of day!")
                sign_in(email, password, company_name)

                delay = randrange(unpunctuality)  # Create new random delay for next day

                lunch_times = set_lunch_times(
                    lunch_time, min_time_to_lunch, max_time_to_lunch
                )
                lunch_delay = randrange(
                    lunch_unpunctuality
                )  # Create new random delay and duration for lunch for next day
                time.sleep(unpunctuality * 60)
            else:
                sign_in(email, password, company_name)

    # Restart the timer
    scheduler.enter(
        TIME_TO_CHECK, 1, main, (scheduler, delay, lunch_delay, lunch_times)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-log",
        "--loglevel",
        default=os.environ["LOG_LEVEL"] if "LOG_LEVEL" in os.environ else "info",
        help="Provide logging level. Example --loglevel debug, default=warning",
    )
    args = parser.parse_args()

    conf_logging(args.loglevel)

    logging.info("Starting application")

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, main, (scheduler, delay, lunch_delay, lunch_times))
    scheduler.run()
