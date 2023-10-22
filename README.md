# Woffu Auto Check-In script

Simple script in that click on `Clock In` and `Clock Out` button inside [Woffu](https://www.woffu.com/en). It detects holidays and only execute it when on working days.


## How to run

1. You need Python 3.6+ and run:
```bash
    pip install -r requirements.txt
```
2. Open `config/secrets.json` file and add your credential and login email.

```json
{
    "email": "",
    "password": "",
    "companyName": "",
    "times": ["09:00", "13:00", "14:00", "17:30"]
}
```
You need to provide the hours you are supposed to click the annoying button. Always an even number, you need to sign in and then sign out.

Execute the following command
```bash
    python3 fuckWoffu.py
```

Forget about everything, it also detect your holidays/pto and do not clock in