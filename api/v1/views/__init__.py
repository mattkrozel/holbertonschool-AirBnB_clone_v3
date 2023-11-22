#!/usr/bin/python3
'''
init file for api v2 views
'''
from flask import Blueprint

views = Blueprint('views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *