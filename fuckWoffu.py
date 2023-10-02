import requests
import json
import time
from datetime import datetime

from SignInWoffu import SignInWoffu

def get_json_data():
    with open('secrets.json', 'r') as file:
        json_content = json.load(file)
        return json_content['email'], json_content['password'], json_content['times'], json_content['companyName']

def is_sign_time(signTimes: [], holidays: list[datetime] = []) -> bool:
    current_time = time.strftime("%H:%M")
    weekday = time.localtime(time.time()).tm_wday
    return current_time in signTimes and weekday not in {5, 6}

'''
    Every 60 seconds I check my enter/leave time and execute request
'''
email, password, sign_times, company_name = get_json_data()
if __name__ == "__main__":
    while True:
        if is_sign_time(sign_times):
            sign_in_app = SignInWoffu(email, password, company_name)
            holidays = sign_in_app.get_holiday()
            success = sign_in_app.sign_in()
            if success:
                print('Fuck woffu -> ', time.strftime("%H:%M"))
            else:
                print('Error maybe something should be done ¯\(ツ)/¯ ',
                      time.strftime("%H:%M"))

        time.sleep(60)
