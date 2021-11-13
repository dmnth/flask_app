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
    
    # ll filters deleted items so you wont have to
    ll = circularList()
    ll.populate(Activitie)

    activities = Activitie.query.filter(Activitie.status!="deleted")
    activitie = ll.get_by_id(id)

    if activitie:

        if request.method == 'POST':
            if request.form.get('next-page'):
                activitie = activitie.get_next()
                return redirect(url_for('details',id=int(activitie.data.id), activitie=activitie.data))

            if request.form.get('prev-page'):
                activitie = activitie.get_prev()
                return redirect(url_for('details',id=int(activitie.data.id), activitie=activitie.data))

            if request.form.get('done'):
                activitie.data.status = 'done'
                act = Activitie.query.get(activitie.data.id)
                act.status = 'done'
                db.session.commit()

            if request.form.get('delete'):
               activitie.data.status = 'deleted'
               act = Activitie.query.get(activitie.data.id)
               act.status = 'deleted'
               db.session.commit()
               activitie = activitie.get_next()
               return redirect(url_for('details', id=activitie.data.id, activitie=activitie.data))

    
        return render_template('activitie.html', id=activitie.data.id, activitie=activitie.data, activities=activities)

    else:
        return render_template('activitie.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    all_selected = False
    # Forms
    form = ActivitieForm()
    delete_form = DeleteForm()

    # Db entities
    activities = Activitie.query.all()
    activitie = Activitie()
    header = \
            Activitie.query.filter(Activitie.header==form.header.data, Activitie.status!='deleted').first()

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

        if request.form.get('select_all'):
            all_selected=True

    return render_template('index.html', form=form, activities=activities,
            delete_form=delete_form, all_selected=all_selected)

@app.route('/jq', methods=['GET', 'POST'])
def jq():
    return render_template('jq.html')

@app.route('/button_test', methods=['GET', 'POST'])
def buttons():
    return render_template('button.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
