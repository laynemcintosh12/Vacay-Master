import unittest
from datetime import datetime
from functions import generate_dates_between, get_itin

class TestFunctions(unittest.TestCase):
    
    def test_generate_dates_between(self):
        start_date_str = "2023-09-20"
        end_date_str = "2023-09-25"

        expected_dates = ["2023-09-20", "2023-09-21", "2023-09-22", "2023-09-23", "2023-09-24", "2023-09-25"]

        generated_dates = generate_dates_between(start_date_str, end_date_str)
        self.assertEqual(generated_dates, expected_dates)


    def test_get_itin(self):
        itinerary_data = [
            {"date": "2023-09-20", "hour": "10:00 AM", "val": "Activity 1"},
            {"date": "2023-09-20", "hour": "02:00 PM", "val": "Activity 2"},
            {"date": "2023-09-21", "hour": "09:00 AM", "val": "Activity 3"},
            {"date": "2023-09-21", "hour": "03:00 PM", "val": "Activity 4"},
        ]

        expected_itinerary = {
            "2023-09-20": {
                "10:00 AM": "Activity 1",
                "02:00 PM": "Activity 2",
            },
            "2023-09-21": {
                "09:00 AM": "Activity 3",
                "03:00 PM": "Activity 4",
            },
        }

        result = get_itin(itinerary_data)
        self.assertEqual(result, expected_itinerary)

if __name__ == '__main__':
    unittest.main()
