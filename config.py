#! /usr/bin/env python3

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "b196aef9bb16f26fe9fc9787fc581ef8256e40be97e17ff9b612f50524f61a0d"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

