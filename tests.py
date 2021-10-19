import unittest
from app import app, db
from app.models import User


# This will be used for testing if some functions in the web application still
# work properly
class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        person = User(username='person')
        person.set_password('password')
        self.assertFalse(person.check_password('wrong password'))
        self.assertTrue(person.check_password('password'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
