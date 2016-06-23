# -*- coding: utf-8 -*-

from flask import Blueprint

bpMain = Blueprint('bpMain', __name__)

from . import views