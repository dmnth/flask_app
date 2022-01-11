#! /usr/bin/env python3

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt
from app import app

# Fetches id for flask-login
# added this comment

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

tasks = db.Table('tasks', 
        db.Column('task_id', db.Integer, db.ForeignKey('activities.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
        )

class Activitie(db.Model):

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(255), index=True, nullable=True)
    status = db.Column(db.String(24), index=True, nullable=True, default='not done')
    header = db.Column(db.String(24), index=True, nullable=True)
    date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    deadline = db.Column(db.DateTime, index=True)
    prioritie = db.Column(db.String(128), index=True, default='maybe tommorow')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
# Self-referent many-to-many entitie
followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
        )

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(124), index=True, unique=True)
    first_name = db.Column(db.String(124), index=True)
    last_name = db.Column(db.String(124), index=True)
    info = db.Column(db.String(255), index=True )
    email = db.Column(db.String(120), index=True, unique=True )
    last_seen = db.Column(db.String(120), index=True )
    hashed_password = db.Column(db.String(255), index=True)
    activities = db.relationship('Activitie', backref='user', lazy='dynamic')
    items = db.relationship('Item', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=3)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), default=None)
    #many-to-many
    # User can have many followers, and can be a follower for many users
    followed = db.relationship('User', secondary=followers,
            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # Assign multiple users on one task, user can have multiple unfinished tasks at once 
    active_tasks = db.relationship('Activitie', secondary=tasks,
            primaryjoin=(tasks.c.task_id == id),
            secondaryjoin=(tasks.c.user_id == id),
            backref = db.backref('users', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"{self.first_name}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=retro&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def has_followers(self):
        return self.followers.count() > 0

    def is_followed(self):
        return self.followed.count() > 0

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def get_followed_activities(self):
        followed_activities = Activitie.query.join(followers, (followers.c.followed_id == Activitie.user_id))\
                .filter(followers.c.follower_id == self.id).order_by(Activitie.date_added.desc())
        return followed_activities

    def get_own_activities(self):
        own_activities = Activitie.query.filter(Activitie.user_id == self.id) 
        return own_activities

    def get_followed_own_activities(self):
        followed_activities = Activitie.query.join(followers, (followers.c.followed_id == Activitie.user_id))\
                .filter(followers.c.follower_id == self.id)
        own_activities = Activitie.query.filter(Activitie.user_id == self.id) 
        return followed_activities.union(own_activities)

    def get_reset_password_token(self, exp_in=600):
        return jwt.encode({'reset_password': self.id, 'exp':time() + exp_in}, app.config['SECRET_KEY'],
                algorithm='HS256')

    def create_assigment(self, form):
        header = form.header.data
        date_added = form.date_added.data
        deadline = form.deadline.data
        description = form.description.data
        user_id = self.id
        new_assigment = Activitie(header=header, date_added=date_added, deadline=deadline, description=description, user_id=user_id)
        db.session.add(new_assigment)
        db.session.commit()
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


# One team can have one person from many departments - front-end, back-end, management
class Team(db.Model):
    
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), index=True)
    members = db.relationship('User', backref='team', lazy='dynamic')



class Role(db.Model):
    
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_name = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f"<{self.name}>"

class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, nullable=False)
    description = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Item {self.name}>"




















