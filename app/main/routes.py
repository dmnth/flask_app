#! /usr/bin/env python3
from app import app
from app.main import main
from .. import db
from flask import render_template, url_for, redirect, session, flash, request, \
        abort
from flask_login import current_user, login_user, logout_user, login_required
from app.main.forms import ActivitieForm, DeleteForm, LoginForm, RegisterForm, EditProfileForm, \
        ResetPasswordRequestForm, ResetPasswordForm
from app.main.models import Activitie, User, Role 
from app.main.queries import Node, circularList 
from app.main.create_roles import create_roles
from app.main.email import send_password_reset_email
from werkzeug.urls import url_parse
from datetime import datetime
import random


@app.before_request
def before_request():
    if current_user.is_authenticated:
        time_now = datetime.utcnow()
        last_seen = time_now.strftime('%m/%d/%Y, %H:%M')
        current_user.last_seen = last_seen 
        db.session.commit()

@app.route('/forgot-password', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check email for further instructions')
        return redirect(url_for('login'))
    
    return render_template('forgot-password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        print('huge bag of dicks here')
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password has been changed, mortal')
        return redirect(url_for('login'))

    return render_template('restore_password.html', form=form)


@app.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    form = ActivitieForm()
    activities = Activitie.query.filter(Activitie.user_id==current_user.id).filter(Activitie.status!="deleted")

    header = \
            Activitie.query.filter(Activitie.header==form.header.data, Activitie.status!='deleted').first()

    # Do stuff here
    if header is None:
        if form.validate_on_submit():
            if not form.dateNotInPast():
                form.deadline.errors.append('Date should not be in past')
            else:
                activitie = Activitie(
                        header=form.header.data,
                        description=form.description.data,
                        status=form.status.data,
                        deadline=form.deadline.data,
                        date_added=form.date_added.data,
                        user_id=current_user.id
                        )
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

@app.route('/explore', methods=['GET'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    activities = Activitie.query.filter(Activitie.status!="deleted").paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=activities.next_num) if activities.has_next else None
    prev_url = url_for('explore', page=activities.prev_num) if activities.has_prev else None
    return render_template('activities_pagination.html', activities=activities.items, next_url=next_url, prev_url=prev_url)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    print(request.args)
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
                activitie = Activitie(
                        header=form.header.data,
                        description=form.description.data,
                        status=form.status.data,
                        deadline=form.deadline.data,
                        date_added=form.date_added.data,
                        user_id=current_user.id
                        )
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

@app.route('/users/<string:user_id>',methods=['GET', 'POST'])
@login_required
def user_page(user_id):
    users = User.query.all()
    form = EditProfileForm(current_user.email, current_user.username)
    add_form = ActivitieForm() 
    viewed_user = User.query.filter_by(id=user_id).first_or_404()
    # This is wrong:
    followed_activities = None
    activities = Activitie.query.filter_by(user_id = viewed_user.id).all()
    role = Role.query.first()
    if not role:
        create_roles()

    if viewed_user.is_followed():
        followed_activities = viewed_user.get_followed_activities()

    if add_form.validate_on_submit():

        if add_form.dateNotInPast():
            current_user.create_assigment(add_form)
        else:
            flash('Date should not be in past')
            add_form.deadline.errors.append('deadline should not be in past')
            print(add_form.errors)
            print(add_form.deadline.errors)

    if request.method == "POST":
        user = User.query.filter_by(id = user_id).first()
        # .get method works with input type only?
        if 'follow' in request.form: 
            current_user.follow(user)

        if 'unfollow' in request.form: 
            current_user.unfollow(user)

        # Make view function for user data editing as well 
        if form.validate():
            

            if form.info.data != current_user.info:
                current_user.info = form.info.data

            if form.role.data != current_user.role:
                role_id = form.role.data
                current_user.role_id = role_id 

#       So this and next if-statments form validations are concurrent

            if form.username.data != current_user.username:
                form.username_validation(form.username)
                if form.username.errors:
                    for error in form.username.errors:
                        print(error)
                else:
                    current_user.username = form.username.data

            if form.email.data != current_user.email:
                form.email_validation(form.email)
                if form.email.errors:
                    for error in form.email.errors:
                        print(error)
                else:
                    current_user.email = form.email.data

        db.session.commit()

    username = viewed_user.username
    email = viewed_user.email
    role = viewed_user.role
    info = viewed_user.info

    return render_template('user_page.html', user_id=viewed_user.id, form=form, user=viewed_user, email=email, username=username, info=info, role=role, users=users, activities=activities, followed_activities=followed_activities, 
            add_form=add_form)

@app.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    viewed_user = User.query.filter(User.id == user_id).first()
    print(viewed_user.username)
    if viewed_user is None:
        flash(f'{viewed_user.username} not found')
        return redirect(url_for('index'))
    if current_user.id == viewed_user.id:
        flash('One should not follow himself')
        return redirect(url_for('user_page', user_id=viewed_user.id))
    current_user.follow(viewed_user)
    db.session.commit()
    flash(f'you are now stalking on {viewed_user.username}')
    return redirect(url_for('user_page', user_id=viewed_user.id))

@app.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    viewed_user = User.query.filter(User.id == user_id).first()
    print(viewed_user.username)
    if viewed_user is None:
        flash(f'{viewed_user.username} not found in db')
        return redirect(url_for('index'))
    if current_user.id == viewed_user.id:
        flash('One should not unfollow himself')
        return redirect(url_for('user_page', user_id=viewed_user.id))
    current_user.unfollow(viewed_user)
    db.session.commit()
    flash(f'you are not stalking on {viewed_user.username}')
    return redirect(url_for('user_page', user_id=viewed_user.id))

@app.route('/activitie/<int:id>/', methods=['GET', 'POST'])
@login_required
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


