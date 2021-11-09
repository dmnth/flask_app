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

@app.route('/activitie/<int:id>/')
def activitie(id):
    return render_template('activitie.html', id=id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    # Forms
    form = ActivitieForm()
    delete_form = DeleteForm()

    # Db entities
    activities = Activitie.query.all()
    activitie = Activitie()
    header = \
            Activitie.query.filter_by(header=form.header.data).first()

    # Do stuff here
    if header is None:
        if form.validate_on_submit():
            if not form.dateNotInPast():
                form.deadline.errors.append('Time travel not allowed')
            else:
                activitie.date_added = form.date_added.data
                activitie.header = form.header.data
                activitie.deadline = form.deadline.data
                activitie.description = form.description.data
                activitie.status = form.status.data
                db.session.add(activitie)
                db.session.commit()
                form.description.data = ''
                return redirect(url_for('index'))

    else:
        flash(f'<\"{form.header.data}\" is already on list somewhere> ')
        form.header.data = ''

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

