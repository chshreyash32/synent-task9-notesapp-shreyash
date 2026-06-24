import unittest
from app import app, db
from models import User, Note

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_status_code(self):
        """Test that home page returns 200"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_contains_expected_text(self):
        """Test that home page contains expected text"""
        response = self.app.get('/')
        self.assertIn(b'Flask Notes', response.data)

    def test_login_page_status_code(self):
        """Test that login page returns 200"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_page_status_code(self):
        """Test that register page returns 200"""
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()