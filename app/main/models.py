#! /usr/bin/env python3

from app import db
from datetime import datetime

class Activitie(db.Model):

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(255), index=True, nullable=False)
    status = db.Column(db.String(24), index=True, nullable=False)
    header = db.Column(db.String(24), index=True, nullable=False)
    date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    deadline = db.Column(db.DateTime, index=True)
    prioritie = db.Column(db.String(128), index=True, default='can wait')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    info = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, nullable=False)
    hashed_password = db.Column(db.String(255), index=True, nullable=False)
    # foreign_keys argument is needed for multiple FK --> single PK
    users = db.relationship('Follower', backref='user', lazy='dynamic', \
            foreign_keys='Follower.user_id')
    followers = db.relationship('Follower', backref='follower', lazy='dynamic', foreign_keys='Follower.follower_id')
    activities = db.relationship('Activitie', backref='user', lazy='dynamic')
    items = db.relationship('Item', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f"<Person {self.name}>"

class Follower(db.Model):

    __tablename__ = 'followers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Role(db.Model):
    
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.relationship('User', backref='role', lazy='dynamic')

class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, nullable=False)
    description = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Item {self.name}>"




















