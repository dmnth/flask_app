#! /usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, \
TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

class ActivitieForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    status = StringField('status', default='not done', \
            validators=[DataRequired()])
    date = DateTimeField('date', default=datetime.utcnow())
    submit = SubmitField()

