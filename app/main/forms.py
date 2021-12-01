#! /usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, \
TextAreaField
from wtforms.validators import DataRequired, InputRequired, EqualTo
from datetime import datetime
from wtforms.widgets import PasswordInput, CheckboxInput
from wtforms.widgets.html5 import EmailInput

class ActivitieForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    status = StringField('status', default='not done', \
            validators=[DataRequired()], id='status-field')
    header = StringField('header', \
            validators=[DataRequired()], id='header-field')
    date_added = DateTimeField('date', format='%y/%m/%d', default=datetime.utcnow(), id='date-field')
    deadline = DateTimeField('deadline', format='%y/%m/%d',id='deadline-field')
    submit = SubmitField(id='submit-btn')

    def dateNotInPast(self):

        difference = self.deadline.data - self.date_added.data
        if difference.days >= 0:
            return True

class DeleteForm(FlaskForm):
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('username')
    email = StringField('email', validators=[DataRequired()], widget=EmailInput())
    password = StringField('password', validators=[InputRequired()], widget=PasswordInput(hide_value=True))
    remember_me = BooleanField(default=False, widget=CheckboxInput())
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()], widget=EmailInput())
    password = StringField('password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')], widget=PasswordInput(hide_value=True))
    confirm = StringField('Re-enter pasword')
    submit = SubmitField()















