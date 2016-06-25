# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from . import bpMain

_all_ = ['index', 'error403', 'error404', 'error500', 'version']


@bpMain.route('/', methods=['GET'])
def index():
    return redirect(url_for('bpAuth.login'))


@bpMain.app_errorhandler(404)
def error403(error):
    return render_template('main/404.html'), 404


@bpMain.app_errorhandler(403)
def error403(error):
    return render_template('main/403.html'), 403


@bpMain.app_errorhandler(500)
def error500(error):
    return render_template('main/500.html'), 500


@bpMain.route('/version', methods=['GET'])
def version():
    packages = []
    pkgs = ['Flask', 'Jinja2', 'peewee', 'gunicorn', 'gevent']

    import sys
    packages.append(dict(name='python', version='{0}.{1}.{2}'.format(*sys.version_info[:3])))

    import pip
    installedPackages = pip.get_installed_distributions()
    for n in pkgs:
        for p in installedPackages:
            if p.project_name == n:
                packages.append(dict(name=p.project_name, version=p.version))

    return render_template('main/version.html', packages=packages)



