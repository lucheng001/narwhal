# -*- coding: utf-8 -*-

from flask import Blueprint

_all_ = ['bpAuth']

bpAuth = Blueprint('bpAuth', __name__)

from . import views

