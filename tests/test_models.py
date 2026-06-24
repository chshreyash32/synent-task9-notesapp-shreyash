import unittest
from app import app, db
from models import User, Note

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """Test user creation and password hashing"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('securepassword')
            db.session.add(user)
            db.session.commit()

            stored_user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(stored_user)
            self.assertTrue(stored_user.check_password('securepassword'))
            self.assertFalse(stored_user.check_password('wrongpassword'))

    def test_note_creation(self):
        """Test note creation and relationship with user"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

            note = Note(title='Test Note', content='This is a test note', user_id=user.id)
            db.session.add(note)
            db.session.commit()

            stored_note = Note.query.filter_by(title='Test Note').first()
            self.assertIsNotNone(stored_note)
            self.assertEqual(stored_note.user_id, user.id)
            self.assertEqual(len(user.notes), 1)

if __name__ == '__main__':
    unittest.main()