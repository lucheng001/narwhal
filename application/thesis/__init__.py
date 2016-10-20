# -*- coding: utf-8 -*-

from flask import Blueprint

_all_ = ['bpThesis']

bpThesis = Blueprint('bpThesis', __name__)

from . import views_add_data
from . import  views_thesis_list