import unittest
from datetime import datetime, timedelta
from src.utils import *


class TestUtils(unittest.TestCase):
    def test_get_json_data(self):
        self.assertIsNotNone(get_json_data())

    def test_is_sign_hour(self):
        sign_times = ["09:00", "18:00"]
        delay = 0
        result = is_sign_hour(sign_times, delay)
        self.assertIsInstance(result, bool)

    def test_is_lunch_time(self):
        lunch_sign_times = ["13:00", "14:00"]
        lunch_delay = 0
        result = is_lunch_time(lunch_sign_times, lunch_delay)
        self.assertIsInstance(result, bool)

    def test_is_end_of_day(self):
        times = ["09:00", "18:00"]
        delay = 0
        result = is_end_of_day(times, delay)
        self.assertIsInstance(result, bool)

    def test_is_holidays(self):
        holidays = [datetime.today()]
        result = is_working_day(holidays)
        self.assertIsInstance(result, bool)

    def test_is_summer_time(self):
        summer_period = [
            datetime.today(),
            datetime.today(),
        ]
        result = is_summer_time(summer_period)
        self.assertIsInstance(result, bool)

    def test_set_lunch_times(self):
        lunch_time = "13:00"
        min_time_to_lunch = 30
        max_time_to_lunch = 60
        result = set_lunch_times(lunch_time, min_time_to_lunch, max_time_to_lunch)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "13:00")
        self.assertGreaterEqual(
            datetime.strptime(result[1], "%H:%M"),
            datetime.strptime(result[0], "%H:%M")
            + timedelta(minutes=min_time_to_lunch),
        )
        self.assertLessEqual(
            datetime.strptime(result[1], "%H:%M"),
            datetime.strptime(result[0], "%H:%M")
            + timedelta(minutes=max_time_to_lunch),
        )

    def test_fix_times_format(self):
        times = ["9:0", "18:0"]
        times_formatted = ["09:00", "18:00"]
        result = fix_times_format(times)
        self.assertIsInstance(result, list)
        self.assertEqual(result, times_formatted)


if __name__ == "__main__":
    unittest.main()
