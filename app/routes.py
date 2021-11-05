#! /usr/bin/env python3

from app import app, db
from flask import render_template, url_for, redirect, session, flash, request
from app.forms import ActivitieForm, DeleteForm
from app.models import Activitie

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
            activitie.date_added = form.date_added.data
            activitie.description = form.description.data
            activitie.status = form.status.data
            activitie.deadline = form.deadline.data
            db.session.add(activitie)
            db.session.commit()
            form.description.data = ''
            return redirect(url_for('index'))
    else:
        flash('Is already in progress')
        form.description.data = ''
    
    act_list = Activitie.query.all()

    if request.method == 'POST': 

        if request.form.get('delete_button'):
            for key in request.form.keys():
                if key.isdigit():
                    Activitie.query.filter(Activitie.id==int(key)).delete()
                    db.session.commit()
                else:
                    print(key)
            return redirect(url_for('index'))
        
        if request.form.get('uncheck_button'):
            print('redirected')
            return redirect(url_for('index'))

    return render_template('index.html', form=form, activities=activities,
            delete_form=delete_form)

