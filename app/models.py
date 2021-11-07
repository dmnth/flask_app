#! /usr/bin/env python3

from app import db
from datetime import datetime

class Activitie(db.Model):

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(255), index=True, nullable=False)
    status = db.Column(db.String(24), index=True, nullable=False)
    date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    deadline = db.Column(db.DateTime, index=True)
    
    def __repr__(self):
        return f"Activitie: {self.description}"

class Person(db.Model):

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    info = db.Column(db.String(255), index=True, nullable=False)
    follower = db.relationship('Follower', backref='following', lazy='dynamic') 


    def __repr__(self):
        return f"<Person {self.name}>"

class Follower(db.Model):

    __tablename__ = 'followers'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


