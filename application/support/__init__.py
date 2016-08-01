# -*- coding: utf-8 -*-

from flask import Blueprint

bpSupport = Blueprint('bpSupport', __name__)

from . import views_support
from . import views_teacher

