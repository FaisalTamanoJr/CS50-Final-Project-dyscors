import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


# This will be used for testing if some functions in the web application still
# work properly
class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        person = User(username='person')
        person.set_password('password')
        self.assertFalse(person.check_password('wrong password'))
        self.assertTrue(person.check_password('password'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
