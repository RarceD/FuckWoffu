import requests
import json

def get_bare_token():
    with open('secrets.json', 'r') as file:
        json_content = json.load(file)
        return json_content['bearerToken']

url = 'https://perkinelmer.woffu.com/api/svc/signs/signs'
headers = {
    'Authorization': 'Bearer ' + get_bare_token(),
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

def fuck_woffu():
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Response:', response.json())
        return True
    else:
        return False

print('fuck woffu script')
fuck_woffu()