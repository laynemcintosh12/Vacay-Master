import os
from unittest import TestCase
from models import db, User, Trip, Itinerary
from app import app

# Set the testing database URL
os.environ['DATABASE_URL'] = "postgresql:///test_vacay"

db.create_all()


class TestItineraryRoutes(TestCase):
    """Test routes related to itineraries."""

    def setUp(self):
        db.drop_all()
        db.create_all()

        # Create a test user
        self.user = User.signup("testuser", "test@test.com", "password", None)
        self.user_id = self.user.id

        # Create a test trip
        self.trip = Trip(name="Test Trip", user_id=self.user_id)
        db.session.add(self.trip)
        db.session.commit()

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def test_get_itinerary_route(self):
        """Test the '/itin/<int:trip_id>' route."""
        with self.client.session_transaction() as sess:
            sess['trip_id'] = self.trip.id
            sess['start_date'] = '2023-09-20'
            sess['end_date'] = '2023-09-25'

        response = self.client.get(f'/itin/{self.trip.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Trip', response.data)

    def test_save_itinerary_route(self):
        """Test the '/save_itinerary' route."""
        with self.client.session_transaction() as sess:
            sess['trip_id'] = self.trip.id

        data = {
            "val": "Test Value",
            "time": "10:00 AM",
            "date": "2023-09-21"
        }

        response = self.client.post('/save_itinerary', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data saved successfully', response.data)

if __name__ == '__main__':
    import unittest

    unittest.main()
