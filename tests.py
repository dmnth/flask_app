#! /usr/bin/env python3

import unittest
from app import app, db
from app.main.models import User, Activitie
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

    def test_avatar(self):
        user=User(username='Jango', email='fettfat@gmail.com')
        self.assertEqual(user.avatar(128), ('https://www.gravatar.com/avatar/192abd819777ab90f75ce868fe16f6cf?d=retro&s=128'))

    def test_follow(self):
        user_1 = User(username='Dick', email='greyson@gmail.com')
        user_2 = User(username='jottaro', email='speedwagon@gmail.com')
        db.session.add_all([user_1, user_2])
        db.session.commit()
        self.assertEqual(user_1.followed.all(), [])
        self.assertEqual(user_2.followed.all(), [])

        user_1.follow(user_2)
        db.session.commit()
        self.assertEqual(user_1.followed.count(), 1)
        self.assertEqual(user_1.followed.first().username, 'jottaro')
        self.assertEqual(user_2.followers.count(), 1)
        self.assertEqual(user_2.followers.first().username, 'Dick')
        self.assertTrue(user_1.is_following(user_2))
        self.assertTrue(user_2.has_followers())
        self.assertTrue(user_1.is_followed())
        user_1.unfollow(user_2)
        self.assertFalse(user_2.is_followed())
        self.assertFalse(user_1.has_followers())

        user_1.unfollow(user_2)
        db.session.commit()
        self.assertFalse(user_1.is_following(user_2))
        self.assertEqual(user_2.followers.count(), 0)
        self.assertEqual(user_1.followed.count(), 0)

    def test_get_activities(self):
        # create some users:
        user_1 = User(username='boris', email='hangman@gmail.com')
        user_2 = User(username='jukko', email='santa_helper12@gmail.com')
        user_3 = User(username='Indulcer', email='nohomo@mail.ru')
        user_4 = User(username='Arcadi', email='theman@mail.ru')
        db.session.add_all([user_1, user_2, user_3, user_4])
        db.session.commit()

        # create some activities:

        act_1 = Activitie(header='Make lunch')
        act_2 = Activitie(header='Steal fish')
        act_3 = Activitie(header='Get free catfood')
        act_4 = Activitie(header='Configure Jynx')
        db.session.add_all([act_1, act_2, act_3, act_4])
        db.session.commit()

        # assign activities to users:

        user_1.activities.append(act_1)
        self.assertEqual(user_1.activities.first().header, 'Make lunch')
        self.assertEqual(user_1.activities.count(), 1)
        user_1.activities.remove(act_1)
        self.assertEqual(user_1.activities.count(), 0)
        db.session.commit()

        user_1.activities.append(act_3)
        user_2.activities.append(act_2)
        user_3.activities.append(act_1)
        user_4.activities.append(act_4)
        db.session.commit()

        # Set follower connections

        user_2.follow(user_1)
        user_3.follow(user_1)
        self.assertTrue(user_2.is_following(user_1))
        self.assertTrue(user_3.is_following(user_1))
        user_1.follow(user_2)
        user_1.follow(user_3)
        self.assertTrue(user_1.is_following(user_2))
        self.assertTrue(user_1.is_following(user_3))
        db.session.commit()

        # get own activities 

        user_1.activities.append(act_3)
        user_1.activities.append(act_4)
        self.assertEqual(user_1.activities.all(), [act_3, act_4])
        self.assertEqual(user_1.get_own_activities().all(), [act_3, act_4])

        # get followed activities

        self.assertEqual(user_1.followed.all(), [user_2, user_3])
        self.assertEqual(user_1.get_followed_activities().all(), [act_2, act_1])

        # get followed + own activities 

        self.assertEqual(user_1.get_followed_own_activities().all(), [act_1, act_2, act_3, act_4])


    def tearDown(self):
        db.session.remove()
        db.drop_all()




if __name__ == "__main__":
    unittest.main(verbosity=2)
