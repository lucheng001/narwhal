# -*- coding: utf-8 -*-

from flask import Blueprint

_all_ = ['bpProgram']

bpProgram = Blueprint('bpProgram', __name__)

from . import views_program
from . import views_teacher
from . import views_department
from . import views_college


