import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from src.utils import *


class TestUtils(unittest.TestCase):

    @patch(
        "src.utils.open",
        new_callable=mock_open,
        read_data='{"email": "test@example.com", "password": "password", "companyName": "test-company", "times": ["09:00", "18:00"], "summer_times": [], "summer_period": [], "unpunctuality": 10, "lunch_unpunctuality": 10, "lunch_time": "13:00", "min_time_to_lunch": 30, "max_time_to_lunch": 60}',
    )
    @patch("src.utils.json.load")
    def test_get_json_data(self, mock_json_load, mock_open):
        mock_json_load.return_value = {
            "email": "test@example.com",
            "password": "password",
            "companyName": "test-company",
            "times": ["09:00", "18:00"],
            "summer_times": [],
            "summer_period": [],
            "unpunctuality": 10,
            "lunch_unpunctuality": 10,
            "lunch_time": "13:00",
            "min_time_to_lunch": 30,
            "max_time_to_lunch": 60,
        }
        result = get_json_data()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "test@example.com")
        self.assertEqual(result[1], "password")
        self.assertEqual(result[2], "test-company")
        self.assertEqual(result[3], ["09:00", "18:00"])
        self.assertEqual(result[4], [])
        self.assertEqual(result[5], None)
        self.assertEqual(result[6], 10)
        self.assertEqual(result[7], 10)
        self.assertEqual(result[8], "13:00")
        self.assertEqual(result[9], 30)
        self.assertEqual(result[10], 60)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_sign_hour(self, mock_datetime):
        sign_times = ["09:00", "18:00"]
        delay = 0
        mock_datetime.today.return_value = datetime(
            year=2024, month=12, day=16, hour=9, minute=0
        )

        result = is_sign_hour(sign_times, delay)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_sign_hour_delay(self, mock_datetime):
        sign_times = ["09:00", "18:00"]
        delay = 5
        mock_datetime.today.return_value = datetime(
            year=2024, month=12, day=16, hour=9, minute=5
        )

        result = is_sign_hour(sign_times, delay)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_sign_hour_false(self, mock_datetime):
        sign_times = ["09:00", "18:00"]
        delay = 0
        mock_datetime.today.return_value = datetime(
            year=2024, month=12, day=16, hour=9, minute=5
        )

        result = is_sign_hour(sign_times, delay)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_lunch_time(self, mock_datetime):
        lunch_sign_times = ["13:00", "14:00"]
        lunch_delay = 0
        mock_datetime.today.return_value = datetime(
            year=2024, month=12, day=16, hour=13, minute=0
        )

        result = is_lunch_time(lunch_sign_times, lunch_delay)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_lunch_time_delay(self, mock_datetime):
        lunch_sign_times = ["13:00", "14:00"]
        lunch_delay = 5
        mock_datetime.today.return_value = datetime(
            year=2024, month=12, day=16, hour=13, minute=5
        )

        result = is_lunch_time(lunch_sign_times, lunch_delay)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_lunch_time_false(self, mock_datetime):
        lunch_sign_times = ["13:00", "14:00"]
        lunch_delay = 0
        mock_datetime.today.return_value = datetime(
            year=2024, month=12, day=16, hour=13, minute=5
        )

        result = is_lunch_time(lunch_sign_times, lunch_delay)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_end_of_day(self, mock_datetime):
        times = ["09:00", "18:00"]
        delay = 0
        result = is_end_of_day(times, delay)
        self.assertIsInstance(result, bool)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_working_day_holidays(self, mock_datetime):
        mock_datetime.today.return_value = datetime(year=2024, month=12, day=16)
        holidays = [datetime(year=2024, month=12, day=16)]
        result = is_working_day(holidays)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_working_day_weekday(self, mock_datetime):
        mock_datetime.today.return_value = datetime(year=2024, month=12, day=16)
        holidays = []
        result = is_working_day(holidays)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_working_day_weekend(self, mock_datetime):
        mock_datetime.today.return_value = datetime(year=2024, month=12, day=21)
        holidays = []
        result = is_working_day(holidays)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    @unittest.mock.patch("src.utils.datetime")
    def test_is_summer_time(self, mock_datetime):
        mock_datetime.today.return_value = datetime(year=2024, month=12, day=21)
        summer_period = [
            datetime(year=2024, month=12, day=21),
            datetime(year=2024, month=12, day=21),
        ]
        result = is_summer_time(summer_period)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

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

    def test_set_lunch_times_no_lunch(self):
        lunch_time = None
        min_time_to_lunch = 30
        max_time_to_lunch = 60
        result = set_lunch_times(lunch_time, min_time_to_lunch, max_time_to_lunch)
        self.assertIsInstance(result, list)
        self.assertListEqual(result, [])

    def test_fix_times_format(self):
        times = ["9:0", "18:0"]
        times_formatted = ["09:00", "18:00"]
        result = fix_times_format(times)
        self.assertIsInstance(result, list)
        self.assertEqual(result, times_formatted)


if __name__ == "__main__":
    unittest.main()
