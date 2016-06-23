# -*- coding: utf-8 -*-

from flask import Blueprint

_all_ = ['bpUser']

bpUser = Blueprint('bpUser', __name__)

from . import views
from . import views_user


