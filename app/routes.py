#! /usr/bin/env python3

from app import app, db
from flask import render_template, url_for, redirect, session, flash, request
from app.forms import ActivitieForm, DeleteForm
from app.models import Activitie
from datetime import datetime
import random

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    # Forms
    form = ActivitieForm()
    delete_form = DeleteForm()

    # Db entities
    activities = Activitie.query.all()
    activitie = Activitie()
    description = \
            Activitie.query.filter_by(description=form.description.data).first()

    # Do stuff here
    if description is None:
        if form.validate_on_submit():
            if form.dateNotInPast() is True:
                activitie.date_added = form.date_added.data
                activitie.deadline = form.deadline.data
                activitie.description = form.description.data
                activitie.status = form.status.data
                db.session.add(activitie)
                db.session.commit()
                form.description.data = ''
                return redirect(url_for('index'))
            else:
                form.deadline.errors.append('Time travel not allowed')

    else:
        flash('Is already not being done. ')
        form.description.data = ''

    if request.method == 'POST': 

        if request.form.get('delete_button'):
            for key in request.form.keys():
                if key.isdigit():
                    Activitie.query.filter(Activitie.id==int(key)).delete()
                    db.session.commit()
            return redirect(url_for('index'))
        
        if request.form.get('uncheck_button'):
            return redirect(url_for('index'))

    return render_template('index.html', form=form, activities=activities,
            delete_form=delete_form)

@app.route('/jq', methods=['GET', 'POST'])
def jq():
    return render_template('jq.html')

