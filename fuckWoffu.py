import requests
import json
import time
from datetime import datetime


def get_json_data():
    with open('secrets.json', 'r') as file:
        json_content = json.load(file)
        return json_content['email'], json_content['password'], json_content['times'], json_content['companyName']


def get_token(email, password, company_name):
    url = "https://" + company_name + ".woffu.com/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "password",
        "username": email,
        "password": password
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return '¯\(ツ)/¯'


def fuck_woffu(token, company_name) -> bool:
    url = "https://" + company_name + ".woffu.com/api/svc/signs/signs"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    payload = {
        "agreementEventId": None,
        "requestId": None,
        "deviceId": "WebApp",
        "latitude": None,
        "longitude": None,
        "timezoneOffset": -120
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 200:
        print('Response:', response.json())
        return True
    else:
        return False


def get_bank_holidays(token, company_name) -> list[datetime]:
    url = "https://" + company_name + ".woffu.com/api/users/calendar-events/next"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, verify=False)
    holidays_list = []
    if response.status_code == 200:
        holidays_array = response.json()
        for day in holidays_array:
            holidays_list.append(datetime.strptime(
                day['Date'], '%Y-%m-%dT%H:%M:%S.%f'))
    return holidays_list


def is_sign_time(signTimes: []) -> bool:
    current_time = time.strftime("%H:%M")
    weekday = time.localtime(time.time()).tm_wday
    return current_time in signTimes and weekday not in {5, 6}


'''
    Every 60 seconds I check my enter/leave time and execute request
'''
email, password, sign_times, company_name = get_json_data()
if __name__ == "__main__":
    current_time = time.strftime("%H:%M")

    bearer_token = get_token(email, password, company_name)
    get_bank_holidays(bearer_token, company_name)

    while True:
        break
        if is_sign_time(sign_times):
            bearer_token = get_token(email, password, company_name)
            success = fuck_woffu(bearer_token, company_name)
            if success:
                print('Fuck woffu -> ', time.strftime("%H:%M"))
            else:
                print('Error maybe something should be done ¯\(ツ)/¯ ',
                      time.strftime("%H:%M"))

        time.sleep(60)
