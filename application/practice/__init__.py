# -*- coding: utf-8 -*-

from flask import Blueprint

_all_ = ['bpPractice']

bpPractice = Blueprint('bpPractice', __name__)

from . import views_teacher
from . import views_practice
from . import views_college
from . import views_department


