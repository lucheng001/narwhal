# -*- coding: utf-8 -*-

from flask import Blueprint

bpNotice = Blueprint('bpNotice', __name__)

from . import views_notice
from . import views_teacher

