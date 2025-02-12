import requests
from datetime import datetime, timedelta
import logging
import time
from src.Telegram import notify
from src.ISignInManager import ISignInManager


MAX_LOGIN_ATTEMPTS = 60

class SignInWoffu(ISignInManager):
    def __init__(self, email, password, company_name):
        self.company_name = company_name
        self.url_path = "https://" + company_name + ".woffu.com/api"
        self.token = self._get_token(email, password)
        self.headers_token = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

    def sign_in(self):
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
            url, json=payload, headers=self.headers_token)
        if response.status_code == 201:
            notify("Sign in/out succesfully")
            logging.info("Sign in/out succesfully")
        else:
            logging.error(
                "Error maybe something should be done. Response code: %s ¯\(ツ)/¯ ",
                response.status_code,
            )

    def get_holiday(self):
        return self._get_bank_holiday() + self._get_pto_holiday()

    def _get_bank_holiday(self):
        url = self.url_path + "/users/calendar-events/next"
        response = requests.get(url, headers=self.headers_token)
        holidays_list = []
        if response.status_code == 200:
            holidays_array = response.json()
            for day in holidays_array:
                holidays_list.append(datetime.strptime(
                    day['Date'], '%Y-%m-%dT%H:%M:%S.%f'))
        else:
            logging.error(
                "Error getting bank holidays. Response code: " + response.status_code
            )
        return holidays_list

    def _get_pto_holiday(self):
        url = self.url_path + "/users/requests/list?pageIndex=0&pageSize=10&statusType=null"
        response = requests.get(url, headers=self.headers_token)
        holidays_list = []
        if response.status_code == 200:
            holidays_array = response.json()
            for day in holidays_array:
                self._calculate_vacation_range(day, holidays_list)
        else:
            logging.error(
                "Error getting PTO holidays. Response code: " + response.status_code
            )
        return holidays_list

    def _calculate_vacation_range(self, day, holidays_list):
        requested_days = int(day['RequestedFormatted']['Values'][0])
        first_day = datetime.strptime(
            day['StartDate'], '%Y-%m-%dT%H:%M:%S.%f')
        if requested_days == 1:
            holidays_list.append(first_day)
            return

        # Detect vacation range:
        last_day = datetime.strptime(
            day['EndDate'], '%Y-%m-%dT%H:%M:%S.%f')
        time_difference = (last_day - first_day).days + 1
        for d in range(time_difference):
            annother_day = first_day + timedelta(days=d)
            holidays_list.append(annother_day)

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

        for attempt in range(MAX_LOGIN_ATTEMPTS):
            try:
                response = requests.post(url, headers=headers, data=data)
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    if token:
                        return token
                    else:
                        logging.error(
                            f"Attempt {attempt + 1}: Token not found in response."
                        )
                        err = "Token not found in response"

                else:
                    logging.error(
                        f"Attempt {attempt + 1}: Error getting token. Response code: {response.status_code}"
                    )
                    err = response.status_code

            except requests.exceptions.ConnectionError as e:
                logging.error(f"Attempt {attempt + 1}: Connection error occurred. {e}")
                err = e
            time.sleep(60)

        error_message = f"Failed to get token after {MAX_LOGIN_ATTEMPTS} attempts. Last error: {err} ¯\(ツ)/¯"
        logging.error(error_message)
        raise Exception(error_message)
