# -*- coding: utf-8 -*-

import datetime
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, login_user, logout_user
from ..constants import CntPermission
from ..models import User
from .forms import LoginForm
from . import bpAuth

_all_ = ['login']


@bpAuth.route('/login', methods=['GET', 'POST'])
def login():
    nextUrl = request.args.get('next', None)
    clientIP = request.remote_addr
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.userName == form.userName.data)
        except User.DoesNotExist:
            user = None
            msg = 'login failed, username:{0}, password:{1}, ip:{2}'
            current_app.logger.warning(msg.format(form.userName.data, form.password.data, form.clientIP.data))
            flash(u'用户名或密码错误', 'error')

        if user and user.verifyPassword(form.password.data):
            user.lastLoginTime = datetime.datetime.now()
            user.save()
            login_user(user)

            if user.password == current_app.config['APP_DEFAULT_PASSWORD']:
                flash(u'请修改密码', 'info')
                return redirect(url_for('bpUser.changePassword'))

            if user.hasPermission(CntPermission.NORMAL):
                return redirect(url_for('bpCourse.taught'))
            else:
                abort(403)

        elif user:
            msg = 'login failed, username:{0}, password:{1}, ip:{2}'
            current_app.logger.warning(msg.format(form.userName.data, form.password.data, form.clientIP.data))
            flash(u'用户名或密码错误', 'error')

    return render_template('auth/login.html', form=form,
                           nextUrl=nextUrl, clientIP=clientIP)


@bpAuth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

