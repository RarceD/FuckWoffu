import sched
import time
import logging
import argparse
from random import randrange
from src.SignInWoffu import *
from src.utils import *


def conf_logging(loglevel):
    logging.basicConfig(
        filename='logs/fuckWoffu.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        level=loglevel.upper())


'''
    Every 60 seconds I check my enter/leave time and execute request
'''
TIME_TO_CHECK = 60
delay = 0
lunch_delay = 0
lunch_duration = 0
lunch_times = None

def main(scheduler, delay, lunch_delay, lunch_duration, lunch_times):
    logging.debug('Starting main function')
    email, password, company_name, times, summer_times, summer_period, unpunctuality, lunch_unpunctuality, lunch_time, min_time_to_lunch, max_time_to_lunch = get_json_data()

    lunch_time = None if lunch_time == "" else lunch_time

    if lunch_times is None:
        lunch_times = set_lunch_times(lunch_time, min_time_to_lunch, max_time_to_lunch)

    sign_in_app = SignInWoffu(email, password, company_name)

    summer = None if not summer_period else [
        datetime.strptime(f"{date}/{datetime.now().year}", "%d/%m/%Y")
        for date in summer_period
    ]

    if is_summer_time(summer): #Summer time
        if (is_sign_hour(summer_times, delay)):
            if is_end_of_day(summer_times, delay):
                time.sleep(randrange(unpunctuality)) # Randomizing time to leave
                delay = randrange(unpunctuality) # Create new random delay for next day

            sign_in(sign_in_app)

    else: #Regular time
        if (is_sign_hour(times, delay) or is_lunch_time(lunch_times, lunch_delay)):
            if is_end_of_day(times, delay):
                time.sleep(randrange(unpunctuality)) # Randomizing time to leave
                delay = randrange(unpunctuality) # Create new random delay for next day

            elif is_end_of_lunch(lunch_times, lunch_delay): # Create new random delay and duration for lunch for next day
                lunch_times = set_lunch_times(lunch_time, min_time_to_lunch, max_time_to_lunch)
                lunch_delay = randrange(lunch_unpunctuality)

            sign_in(sign_in_app)

    # Restart the timer
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler, delay, lunch_delay, lunch_duration, lunch_times))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-log',
                        '--loglevel',
                        default='warning',
                        help='Provide logging level. Example --loglevel debug, default=warning' )
    args = parser.parse_args()
    
    conf_logging(args.loglevel)

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler, delay, lunch_delay, lunch_duration, lunch_times))
    scheduler.run()
