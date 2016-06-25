# -*- coding: utf-8 -*-

from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from playhouse.flask_utils import FlaskDB


_all_ = ['csrf', 'db', 'lm']

csrf = CsrfProtect()

db = FlaskDB()

lm = LoginManager()

