import os
from unittest import TestCase
from models import db, User
from app import app

# Set the testing database URL
os.environ['DATABASE_URL'] = "postgresql:///test_vacay"

db.create_all()


class TestUserRoutes(TestCase):
    """Test routes related to user authentication and registration."""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def test_signup_route(self):
        """Test the '/signup' route."""
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@test.com"
        }

        response = self.client.post('/signup', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome testuser!', response.data)

    def test_login_route(self):
        """Test the '/login' route."""
        # Create a test user
        user = User.signup("testuser", "test@test.com", "testpassword", None)
        db.session.commit()

        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome testuser!', response.data)

    def test_logout_route(self):
        """Test the '/logout' route."""
        # Create a test user and log them in
        user = User.signup("testuser", "test@test.com", "testpassword", None)
        db.session.commit()
        self.client.post('/login', data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'testuser', response.data)
        self.assertIn(b'You have been logged out', response.data)

if __name__ == '__main__':
    import unittest

    unittest.main()
