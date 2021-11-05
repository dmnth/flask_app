#! /usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, \
TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

class ActivitieForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    status = StringField('status', default='not done', \
            validators=[DataRequired()], id='status-field')
    date_added = DateTimeField('date', default=datetime.utcnow(), id='date-field')
    deadline = DateTimeField('deadline', id='deadline-field')
    submit = SubmitField(id='submit-btn')

class DeleteForm(FlaskForm):
    submit = SubmitField()
