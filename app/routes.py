#! /usr/bin/env python3

from app import app, db
from flask import render_template, url_for, redirect, session, flash, request, \
        abort
from app.forms import ActivitieForm, DeleteForm
from app.models import Activitie
from app.queries import Node, circularList 
from datetime import datetime
import random

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/activitie/<int:id>/', methods=['GET', 'POST'])
def details(id):
    activitie = Activitie.query.get(id)
    if not activitie:
        return render_template('404.html')

    activities = Activitie.query.all()
    ll = circularList()
    ll.populate(Activitie)
    activitie = ll.get_by_id(id)

    if request.method == 'POST':
        if request.form.get('next-page'):
            activitie = activitie.get_next()
            return redirect(url_for('details',id=int(activitie.data.id), activitie=activitie))

        if request.form.get('prev-page'):
            activitie = activitie.get_prev()
            return redirect(url_for('details',id=int(activitie.data.id), activitie=activitie))

        if request.form.get('done'):
            activitie.data.status = 'done'
            act = Activitie.query.get(activitie.data.id)
            act.status = 'done'
            db.session.commit()

        if request.form.get('delete'):
           activitie.data.status = 'delete'
           act = Activitie.query.get(activitie.data.id)
           act.status = 'delete'
           db.session.commit()
           activitie = activitie.get_next()
           return redirect(url_for('details', id=activitie.data.id, activitie=activitie))
    
    return render_template('activitie.html', id=activitie.data.id, activitie=activitie, activities=activities)

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

@app.route('/button_test', methods=['GET', 'POST'])
def buttons():
    return render_template('button.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
