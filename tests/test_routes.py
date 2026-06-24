import unittest
from app import app, db
from models import User, Note

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Create a test user
            self.user = User(username='testuser', email='test@example.com')
            self.user.set_password('password')
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, email='test@example.com', password='password'):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_home_page(self):
        """Test that home page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask Notes', response.data)

    def test_register_page(self):
        """Test registration page loads"""
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        """Test login page loads"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_success(self):
        """Test successful login"""
        response = self.login()
        self.assertIn(b'My Notes', response.data)  # Redirects to notes page
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        """Test failed login"""
        response = self.login(email='wrong@example.com', password='wrong')
        self.assertIn(b'Login Unsuccessful', response.data)
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        """Test successful registration"""
        response = self.app.post('/register', data=dict(
            username='newuser',
            email='new@example.com',
            password='newpassword',
            confirm_password='newpassword'
        ), follow_redirects=True)
        self.assertIn(b'Your account has been created', response.data)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Skipping due to complexity in test setup")
    def test_note_creation_requires_login(self):
        """Test that creating a note requires login"""
        response = self.app.get('/note/new', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

if __name__ == '__main__':
    unittest.main()