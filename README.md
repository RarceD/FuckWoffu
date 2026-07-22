# 🕒 FuckWoffu — Woffu Auto Check-In

**Stop babysitting the clock-in button.** FuckWoffu is a tiny Python service that automatically clicks `Clock In` and `Clock Out` for you in [Woffu](https://www.woffu.com/en) — at the right times, on working days only, skipping your holidays and PTO, and even randomizing your entry/leave/lunch so it looks convincingly human.

Set it once. Forget it forever.


---

## ⏳ How much time does manual check-in actually waste?

It feels like nothing — a couple of clicks. But add it up:

- Open the app/website, wait for it to load, find the button, click **Clock In**. Repeat for lunch out, lunch back, and **Clock Out**.
- Realistically **~1–2 minutes per interaction**, 4 interactions a day.

| Cadence | Time per day | Per work week | Per month (~22 days) | Per year (~220 days) |
| --- | --- | --- | --- | --- |
| **~1 min × 4 clicks** | ~4 min | ~20 min | ~1h 28m | **~14.7 hours** |
| **~2 min × 4 clicks** | ~8 min | ~40 min | ~2h 56m | **~29.3 hours** |

That's **up to ~4 full working days a year** spent clicking a button — not counting the days you *forget* to clock in and have to email HR to fix your timesheet. 😬

FuckWoffu drops that to **zero**.

---

## ✨ Features

- ⏰ **Automatic clock in / out** at your configured times.
- 📅 **Working-days only** — skips weekends automatically.
- 🏖️ **Holiday & PTO aware** — reads your Woffu calendar and stays quiet on days off.
- 🍽️ **Lunch break support** with a **randomized duration** every day.
- 🎲 **Human-like unpunctuality** — randomizes entry, leave and lunch times so you're never suspiciously precise.
- ☀️ **Summer schedule** — different hours for a configurable summer period.
- 📝 **Logging** with configurable levels for peace of mind.
- 🐳 **Docker-ready** — run it as a container and never think about it again.

---

## 🚀 Set up

1. You need **Python 3.6+**, then install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Open `config/config.json` and add your Woffu credentials, login email and company name:

    ```json
    {
        "email": "",
        "password": "",
        "companyName": ""
    }
    ```

3. Set the hours you'd otherwise click the annoying button. First value signs you in, last signs you out:

    ```json
    {
        "times": ["09:00", "18:00"]
    }
    ```

4. (Optional) Add a lunch time to clock out, plus the minimum and maximum lunch duration — it gets randomized every day:

    ```json
    {
        "lunch_time": "13:00",
        "min_time_to_lunch": 30,
        "max_time_to_lunch": 60
    }
    ```

5. If you don't take a lunch break, just leave the time empty:

    ```json
    {
        "lunch_time": ""
    }
    ```

6. (Optional) Randomize your entry, leave and lunch times to look more human. Set the maximum unpunctuality (in minutes) for entry/leave and for lunch:

    ```json
    {
        "unpunctuality": 10,
        "lunch_unpunctuality": 30
    }
    ```

7. (Optional) If you have a summer schedule, fill in the summer times and the start/end day (no year needed):

    ```json
    {
        "summer_times": ["08:00", "15:00"],
        "summer_period": ["1/8", "31/8"]
    }
    ```

Forget about everything else — it also detects your holidays/PTO and won't clock in on those days.

---

## ▶️ Run with Python

```bash
python3 fuckWoffu.py
```

Run as a background service without logs:

```bash
nohup python3 fuckWoffu.py &
```

Set the logging level (e.g. `debug`, `info`, `warning`):

```bash
python3 fuckWoffu.py --loglevel debug
```

Logs are written to `logs/fuckWoffu.log`.

---

## 🐳 Run with Docker

### Manually build the image and run the container

```sh
docker build -t py-woffu-app .
docker run py-woffu-app
```

### Directly with Compose

```sh
docker compose up
```

---

## ⚠️ Disclaimer

This tool is intended for personal automation of your own attendance. Make sure automating your check-in complies with your company's policies and your local labor regulations. Use responsibly.
