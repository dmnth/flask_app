#! /usr/bin/evn python3

from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, forms, models, queries, errors
