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
        if (self.deadline.data - self.date_added.data).days >= 0: 
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
    choices = [(1, 'normal'), (2, 'front-end'), (3, 'back-end')]
    info = TextAreaField('about')
    role = SelectField('about',choices=choices)
    username = StringField('username')
    email = StringField('email', widget=EmailInput())
    submit = SubmitField()

    # Initialization
    def __init__(self, current_email, current_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.current_email = current_email
        self.current_username = current_username

    # Validation of current email

    def email_validation(self, email):
        if email.data != self.current_email:
            this_email = User.query.filter_by(email=self.email.data).first()
            if this_email is not None:
                self.email.errors.append('This email is already registered')
                raise ValidationError('This email is already registered')

            
    def username_validation(self, username):
        if username.data != self.current_username:
            this_user = User.query.filter_by(username=self.username.data).first()
            if this_user is not None:
                self.username.errors.append('This username is already taken')
                raise ValidationError('This username is already taken')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()], widget=EmailInput())
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = StringField('password', validators=[InputRequired()], widget=PasswordInput(hide_value=True))
    password_repeat= StringField('Re-enter pasword', validators=[EqualTo('password', message='Passwords must match')], widget=PasswordInput(hide_value=True))
    submit = SubmitField('Change password')



