import requests
import json
import time


def get_json_data():
    with open('secrets.json', 'r') as file:
        json_content = json.load(file)
        return json_content['bearerToken'], json_content['times']


bearer_token, sign_times = get_json_data()
url = 'https://perkinelmer.woffu.com/api/svc/signs/signs'
headers = {
    'Authorization': 'Bearer ' + bearer_token,
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


def fuck_woffu() -> bool:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Response:', response.json())
        return True
    else:
        return False


def is_sign_time(signTimes: []) -> bool:
    current_time = time.strftime("%H:%M")
    if current_time in signTimes:
        return True
    return False


'''
    Every 60 seconds I check my enter/leave time and execute request
'''
if __name__ == "__main__":
    while True:

        if is_sign_time(sign_times):
            success = fuck_woffu()
            if success:
                print('Fuck woffu -> ', time.strftime("%H:%M"))
            else:
                print('Error maybe something should be done ¯\_(ツ)_/¯ ',
                      time.strftime("%H:%M"))

        time.sleep(60)
