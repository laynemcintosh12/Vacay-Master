import os
from unittest import TestCase
from models import db, User, Destination, Trip
from app import app

# Set the testing database URL
os.environ['DATABASE_URL'] = "postgresql:///test_vacay"

db.create_all()


class TestDestinationRoutes(TestCase):
    """Test routes related to destinations."""

    def setUp(self):
        db.drop_all()
        db.create_all()

        # Create a test user
        self.user = User.signup("testuser", "test@test.com", "password", None)
        self.user_id = self.user.id

        # Create a test destination
        self.destination = Destination(name="Test Destination", description="Test description")
        db.session.add(self.destination)
        db.session.commit()

        # Create a test trip
        self.trip = Trip(name="Test Trip", user_id=self.user_id)
        db.session.add(self.trip)
        db.session.commit()

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def test_get_destinations_route(self):
        """Test the '/dest' route."""
        response = self.client.get('/dest')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Destination', response.data)

    def test_get_blog_route(self):
        """Test the '/blog/<int:dest_id>' route."""
        response = self.client.get(f'/blog/{self.destination.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Destination', response.data)

    def test_new_post_route(self):
        """Test the '/newpost/<int:dest_id>' route."""
        with self.client.session_transaction() as sess:
            sess['trip_id'] = self.trip.id

        response = self.client.get(f'/newpost/{self.destination.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a new post', response.data)

    def test_new_comment_route(self):
        """Test the '/newcomment/<int:post_id>' route."""
        response = self.client.get(f'/newcomment/{self.destination.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a new comment', response.data)

    def test_delete_post_route(self):
        """Test the '/delete_post/<int:post_id>' route."""
        response = self.client.post(f'/delete_post/{self.destination.id}')
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion



if __name__ == '__main__':
    import unittest

    unittest.main()
