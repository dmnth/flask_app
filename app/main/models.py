#! /usr/bin/env python3

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

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
    description = db.Column(db.Text(255), index=True, nullable=False)
    status = db.Column(db.String(24), index=True, nullable=False)
    header = db.Column(db.String(24), index=True, nullable=False)
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
    #many-to-many
    followed = db.relationship('User', secondary=followers,
            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0



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




















