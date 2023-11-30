import requests
import os

def notify(message):
    apiToken = os.environ.get('WOFFU_TELEGRAM_APITOKEN', None)
    chatID = os.environ.get('WOFFU_TELEGRAM_CHATID', None)

    if apiToken is None or chatID is None: 
        return

    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    except Exception as e:
        pass