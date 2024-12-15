# Woffu Auto Check-In script

Simple script in that click on `Clock In` and `Clock Out` button inside [Woffu](https://www.woffu.com/en). It detects holidays and only execute it when on working days.

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FRarceD%2FFuckWoffu&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Hits%3A&edge_flat=false)](https://hits.seeyoufarm.com)

## Set up

1. You need Python 3.6+ and run:

```bash
pip install -r requirements.txt
```

2. Open `config/secrets.json` file and make the following changes:

Add your credential, login email and company name.

```json
{
    "email": "",
    "password": "",
    "companyName": ""
}
```

You need to provide the hours you are supposed to click the annoying button. Always an even number, you need to sign in and then sign out.

```json
{
    "times": ["09:00", "18:00"]
}
```

You can add your lunch time to clock out and the minimun and maximun duration of your lunch, it will be randomized everyday.

```json
{
    "lunch_time": "13:00",
    "min_time_to_lunch": 30,
    "max_time_to_lunch": 60
}
```

If you don't have lunch break, just leave the time empty.

```json
{
    "lunch_time": "",
}
```

There is an option to randomize your entry, leave and lunch time to look more human. You just have to set the maximun unpunctuality for your entry and lunch.

```json
{
    "unpunctuality": 10,
    "lunch_unpunctuality": 30
}
```


If you have summer time (maybe it doesn't exist in your country) fill it with the times like the regular ones and the starting and ending day withouth the year like in this example:

```json
{
    "summer_times": ["08:00", "15:00"],
    "summer_period": ["1/8", "31/8"]
}
```

Forget about everything else, it also detect your holidays/pto and do not clock in.

## Run with python

Execute the following command:

```bash
python3 fuckWoffu.py
```

Run as background service without logs:

```bash
nohup python3 fuckWoffu.py &
```

## Run with docker

Manually create image and run container:

```sh
docker build -t py-woffu-app .
docker run py-woffu-app
```

Directly by composer:

```sh
docker compose up
```
