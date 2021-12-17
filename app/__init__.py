#! /usr/bin/env python3

from flask import Flask
from config import config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

app = Flask(__name__)
app.config.from_object(config['development'])
login = LoginManager(app)
# endpoint of function that handles login's
login.login_view='login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.main import forms, routes, models, errors

