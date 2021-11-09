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
    header = StringField('header', default='Your header', \
            validators=[DataRequired()], id='header-field')
    date_added = DateTimeField('date', format='%y/%m/%d', default=datetime.utcnow(), id='date-field')
    deadline = DateTimeField('deadline', format='%y/%m/%d',id='deadline-field')
    submit = SubmitField(id='submit-btn')

    def dateNotInPast(self):

        difference = self.deadline.data - self.date_added.data
        print(difference.days)
        if difference.days >= 0:
            return True
        else:
            return False


class DeleteForm(FlaskForm):
    submit = SubmitField()
