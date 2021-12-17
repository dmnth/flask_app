#! /usr/bin/env python3

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 


app = Flask(__name__)
app.config.from_object(config['default'])
login = LoginManager(app)
# endpoint of function that handles login's
login.login_view='login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.main import forms, routes, models, errors

# port < 8085
if not app.debug and not app.testing:

    # logging to file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/not_done.log', maxBytes=10240,
            backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Not done startup')
    
    # Getting logs by email
    if app.config['MAIL_SERVER']:
        auth=None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure=None
        if app.config['MAIL_USE_TLS']:
            secure=()
        mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Failure',
                credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
