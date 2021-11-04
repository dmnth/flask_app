#! /usr/bin/env python3

from app import app
from flask import render_template, url_for, redirect, session
from app.forms import ActivitieForm
from app.models import Activitie

@app.route('/')
@app.route('/index')
def index():
    form = ActivitieForm()
    return render_template('index.html', form=form)

