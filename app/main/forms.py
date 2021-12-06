#! /usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, InputRequired, EqualTo
from datetime import datetime
from wtforms.widgets import PasswordInput, CheckboxInput, TextArea, Select
from wtforms.widgets.html5 import EmailInput
from app.main.models import User

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
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()], widget=EmailInput())
    password = StringField('password', validators=[InputRequired()], widget=PasswordInput(hide_value=True))
    confirm = StringField('Re-enter pasword', validators=[EqualTo('password', message='Passwords must match')], widget=PasswordInput(hide_value=True))
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class EditProfileForm(FlaskForm):
    choices = [(1, 'front-end'), (2, 'back-end'), (3, 'normal')]
    info = TextAreaField('about', default='Write about yourself')
    role = SelectField('about',choices=choices)
    username = StringField('username')
    submit = SubmitField()













