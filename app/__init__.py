#! /usr/bin/env python3

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#from app.main import main as main_blueprint
#app.register_blueprint(main_blueprint)

from app.main import forms, routes, models

