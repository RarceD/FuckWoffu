import sched
import time
import logging
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
    email, password, company_name, times, summer_times, summer_period = get_json_data()
    
    sign_in_app = SignInWoffu(email, password, company_name)

    summer = [
        datetime.strptime(f"{date}/{datetime.now().year}", "%d/%m/%Y").time()
        for date in summer_period
        ]

    if is_sign_hour(summer_times if is_summer_time(summer_period) else times):
        sign_in(sign_in_app)

    # Restart the timer
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))


if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(TIME_TO_CHECK, 1, main, (scheduler,))
    scheduler.run()
