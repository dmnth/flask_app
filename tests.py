#! /usr/bin/env python3

import unittest
from app import app, db
from app.main.models import User
from datetime import datetime

class userModelTest(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def test_password_hashing(self):
        user = User(username='Jango')
        user.set_password('bobbasbubbas')
        self.assertFalse(user.check_password('bibbasbobbas'))
        self.assertTrue(user.check_password('bobbasbubbas'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main(verbosity=2)
