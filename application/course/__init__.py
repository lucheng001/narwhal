# -*- coding: utf-8 -*-

from flask import Blueprint

_all_ = ['bpCourse']

bpCourse = Blueprint('bpCourse', __name__)

from . import views_teacher
from . import views_course

