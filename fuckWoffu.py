import json
import time
from datetime import datetime

from SignInWoffu import SignInWoffu


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


def main():
    email, password, sign_times, company_name = get_json_data()
    if is_sign_hour(sign_times):
        sign_in_app = SignInWoffu(email, password, company_name)
        holidays = sign_in_app.get_holiday()
        if not is_holidays(holidays):
            success = sign_in_app.sign_in()
            if success:
                print('Fuck woffu -> ', time.strftime("%H:%M"))
            else:
                print('Error maybe something should be done ¯\(ツ)/¯ ',
                      time.strftime("%H:%M"))


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
