from ISignInManager import ISignInManager
import requests
from datetime import datetime


class SignInWoffu(ISignInManager):
    def __init__(self, email, password, company_name):
        self.company_name = company_name
        self.url_path = "https://" + company_name + ".woffu.com/api"
        self.token = self._get_token(email, password)
        self.headers_token = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

    def sign_in(self) -> bool:
        url = self.url_path + "/svc/signs/signs"
        payload = {
            "agreementEventId": None,
            "requestId": None,
            "deviceId": "WebApp",
            "latitude": None,
            "longitude": None,
            "timezoneOffset": -120
        }
        response = requests.post(
            url, json=payload, headers=self.headers_token, verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_holiday(self):
        return self._get_bank_holiday() + self._get_pto_holiday()

    def _get_bank_holiday(self) -> list[datetime]:
        url = self.url_path + "/users/calendar-events/next"
        response = requests.get(url, headers=self.headers_token, verify=False)
        holidays_list = []
        if response.status_code == 200:
            holidays_array = response.json()
            for day in holidays_array:
                holidays_list.append(datetime.strptime(
                    day['Date'], '%Y-%m-%dT%H:%M:%S.%f'))
        return holidays_list

    def _get_pto_holiday(self) -> list[datetime]:
        url = self.url_path + "/users/requests/list?pageIndex=0&pageSize=10&statusType=20"
        response = requests.get(url, headers=self.headers_token, verify=False)
        holidays_list = []
        if response.status_code == 200:
            holidays_array = response.json()
            for day in holidays_array:
                holidays_list.append(datetime.strptime(
                    day['StartDate'], '%Y-%m-%dT%H:%M:%S.%f'))
        return holidays_list

    def _get_token(self, email, password):
        url = "https://" + self.company_name + ".woffu.com/token"
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
