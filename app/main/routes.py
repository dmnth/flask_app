#! /usr/bin/env python3
from app import app
from app.main import main
from .. import db
from flask import render_template, url_for, redirect, session, flash, request, \
        abort
from flask_login import current_user, login_user, logout_user, login_required
from app.main.forms import ActivitieForm, DeleteForm, LoginForm, RegisterForm
from app.main.models import Activitie, User 
from app.main.queries import Node, circularList 
from werkzeug.urls import url_parse
from datetime import datetime
import random


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
#       network location <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/activitie/<int:id>/', methods=['GET', 'POST'])
def details(id):
    
    # ll filters deleted items so you wont have to
    # is used for left menu, because of reasons...
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

            if request.form.get('edit'):
               return redirect(url_for('details', edit=True,
                   id=activitie.data.id)) 

            if request.form.get('list'):
                return redirect(url_for('activities'))


        return render_template('activitie.html', id=int(activitie.data.id), activitie=activitie.data, 
            activities=activities)

    else:
        return render_template('activitie.html')

@app.route('/activities', methods=['GET', 'POST'])
def activities():
    form = ActivitieForm()
    activities = Activitie.query.filter(Activitie.status!="deleted")
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
                return redirect(url_for('activities'))

    else:
        flash(f'<\"{form.header.data}\" is already on list somewhere> ')
        form.header.data = ''


    if request.method == "POST":

        if request.form.get('single'):
            activitie = Activitie.query.filter_by(status="not done").first()
            return redirect(url_for('details', id=activitie.id, activitie=activitie)) 

        if request.form.get('delete'):
            id = request.form.get('id')
            act = Activitie.query.get(id)
            if act:
                act.status = 'deleted'
                db.session.commit()

        if request.form.get('done'):
            id = request.form.get('id')
            act = Activitie.query.get(id)
            if act:
                act.status = 'done'
                db.session.commit()

    return render_template('activities_long.html', activities=activities, form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    all_selected = False
    # Forms
    form = ActivitieForm()
    delete_form = DeleteForm()

    # Db entities
    activities = Activitie.query.filter(Activitie.status != 'deleted')
    activitie = Activitie()
    header = \
            Activitie.query.filter(Activitie.header==form.header.data, Activitie.status!='deleted').first()

    # Priorities:
    choices = ['not_today', 'not_important', 'maybe_tommorow']

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
                activitie.user_id = current_user.id
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
        
        if request.form.get('Select'):
            all_selected=True

        if request.form.get('deSelect'):
            all_selected=False

        if request.form.get('prior'):
            id = request.form.get('id')
            act = Activitie.query.get(id)
            new_prioritie = request.form.get('prior')
            idx = choices.index(new_prioritie)
            temp = choices[0]
            choices[0] = choices[idx]
            choices[idx] = temp
            print(choices)
            act.prioritie = new_prioritie 
            db.session.commit()

    return render_template('index.html', form=form, activities=activities,
            delete_form=delete_form, all_selected=all_selected,
            choices=choices)

@app.route('/jq', methods=['GET', 'POST'])
def jq():
    return render_template('jq.html')

@app.route('/button_test', methods=['GET', 'POST'])
def buttons():
    return render_template('button.html')

@app.route('/text', methods=['GET', 'POST'])
def text():
    return render_template('text.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
