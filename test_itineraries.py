import unittest
from unittest import TestCase
from app import app
from models import db, Trip, User, Itinerary
import json

class TestItineraryApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///vacay-test'
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_data(self):
        # Create test data (trips, users, itineraries) for testing
        user = User(username='test_user')
        trip = Trip(name='Test Trip', start_date='2023-09-30', end_date='2023-10-05', user=user)
        itinerary = Itinerary(user_id=user.user_id, trip_id=trip.trip_id, date='2023-10-01', hour='8:00 AM', val='Test Value')
        db.session.add(user)
        db.session.add(trip)
        db.session.add(itinerary)
        db.session.commit()

    def test_get_itinerary(self):
        self.create_test_data()

        response = self.client.get('/itin/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Trip', response.data)
        self.assertIn(b'2023-09-30', response.data)
        self.assertIn(b'Test Value', response.data)
        self.assertIn(b'8:00 AM', response.data)
        self.assertIn(b'2023-10-01', response.data)

    def test_save_itinerary(self):
        data = {
            'val': 'Test Value',
            'time': '8:00 AM',
            'date': '2023-09-30'
        }
        response = self.client.post('/save_itinerary', json=data)
        self.assertEqual(response.status_code, 200)
        saved_itinerary = Itinerary.query.first()
        self.assertIsNotNone(saved_itinerary)
        self.assertEqual(saved_itinerary.val, 'Test Value')
        self.assertEqual(saved_itinerary.hour, '8:00 AM')
        self.assertEqual(saved_itinerary.date, '2023-09-30')
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['message'], 'Data saved successfully')

if __name__ == '__main__':
    unittest.main()
