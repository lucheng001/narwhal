# -*- coding: utf-8 -*-

import hashlib
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user
from ..models import User
from ..constants import CntRoles, CntPermission
from .forms import RegisterForm, ChangePasswordForm, ChangeChineseNameForm
from . import bpUser


@bpUser.route('/register', methods=['GET', 'POST'])
def register():
    c = request.args.get('c', None)
    if c is None or len(c) != 8:
        flash('暂不开放注册', 'info')
        return redirect(url_for('bpAuth.login'))

    vc = c[0::2].encode('utf-8')
    ic = c[1::2].encode('utf-8')
    verificationCode = hashlib.sha1(vc).hexdigest()
    invitationCode = hashlib.sha1(ic).hexdigest()

    form = RegisterForm()
    if form.validate_on_submit():
        import re
        from werkzeug.security import generate_password_hash
        User.create(
            userName=re.sub('[\s+]', '', form.userName.data),
            chineseName=re.sub('[\s+]', '', form.chineseName.data),
            role=CntRoles.TEACHER.label,
            permission=CntRoles.getRolePermission(CntRoles.TEACHER.label),
            password=form.password.data,
            passwordHash=generate_password_hash(form.password.data)
        )
        flash(u'注册成功，请重新登录', 'success')
        return redirect(url_for('bpAuth.login'))

    return render_template('user/register.html', form=form, c=c,
                           verificationCode=verificationCode, invitationCode=invitationCode)


@bpUser.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user
    return render_template('user/profile.html', user=user)


@bpUser.route('/change/password', methods=['GET', 'POST'])
@login_required
def changePassword():
    user = current_user._get_current_object()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        from werkzeug.security import generate_password_hash
        if user.verifyPassword(form.oldPassword.data):
            user.password = form.newPassword.data
            user.passwordHash = generate_password_hash(form.newPassword.data)
            user.save()
            logout_user()
            flash(u'密码修改成功，请重新登录', 'success')
            return redirect(url_for('bpAuth.login'))
        else:
            flash(u'旧密码错误', 'error')

    return render_template('user/changePassword.html', form=form)


@bpUser.route('/change/ChineseName', methods=['GET', 'POST'])
@login_required
def changeChineseName():
    user = current_user._get_current_object()
    form = ChangeChineseNameForm()
    if form.validate_on_submit():
        import re
        user.chineseName = re.sub('[\s+]', '', form.chineseName.data)
        user.save()
        logout_user()
        flash(u'姓名修改成功，请重新登录', 'success')
        return redirect(url_for('bpAuth.login'))

    return render_template('user/changeChineseName.html', form=form)


