# -*- coding: utf-8 -*-

import os
import multiprocessing

_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
_APP_DIR = os.path.abspath(os.path.dirname(_BASE_DIR))
_CPU_COUNT = multiprocessing.cpu_count()

chdir = _APP_DIR
pythonpath = _APP_DIR
# bind = 'unix:' + os.path.join(_APP_DIR, 'run', 'application.sock')
bind = '0.0.0.0:5000'
pidfile = os.path.join(_APP_DIR, 'run', 'app.pid')
accesslog = os.path.join(_APP_DIR, 'logs', 'access.gunicorn.log')
errorlog = os.path.join(_APP_DIR, 'logs', 'error.gunicorn.log')
max_requests = 500
workers = _CPU_COUNT if _CPU_COUNT > 8 else _CPU_COUNT * 2 + 1
worker_class = 'gevent'
daemon = True
user = 'narwhal'
group = 'narwhal'

