# Woffu Auto Check-In script

Simple script in that click on `Clock In` and `Clock Out` button inside [Woffu](https://www.woffu.com/en). It detects holidays and only execute it when on working days.

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FRarceD%2FFuckWoffu&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Hits%3A&edge_flat=false)](https://hits.seeyoufarm.com)

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

Run as background service without logs:
```bash
nohup python3 fuckWoffu.py &
```

Forget about everything, it also detect your holidays/pto and do not clock in

# Run with docker:

Manually create image and run container:
```sh
docker build -t py-woffu-app .
docker run py-woffu-app
```

Directly by composer:
```sh
docker compose up
```
