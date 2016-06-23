# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from playhouse.flask_utils import get_object_or_404
from ..models import User, Course
from ..utilities import permission_required, generate_random_string
from ..constants import CntRoles, CntPermission
from .forms_user import AddUserForm
from . import bpUser


@bpUser.route('/add', methods=['GET', 'POST'])
def add():
    form = AddUserForm()
    if form.validate_on_submit():
        import re
        from werkzeug.security import generate_password_hash
        User.create(
            userName=re.sub('[\s+]', '', form.userName.data),
            chineseName=re.sub('[\s+]', '', form.chineseName.data),
            role=form.role.data,
            password=form.password.data,
            passwordHash=generate_password_hash(form.password.data)
        )
        flash(u'注册成功，请重新登录', 'success')
        return redirect(url_for('bpAuth.login'))

    return render_template('user/instructor/register.html', form=form)


@bpUser.route('/resetPassword/<int:userId>', methods=['GET'])
@login_required
@permission_required(CntPermission.USER)
def resetPassword(courseId, studentId):
    student = get_object_or_404(User, (User.id == studentId))
    if student.role != CntRoles.STUDENT.label:
        abort(403)

    course = get_object_or_404(Course, (Course.id == courseId))
    me = current_user
    instructor = course.creator
    if instructor.id != me.id:
        abort(403)

    from werkzeug.security import generate_password_hash
    newPassword = generate_random_string()
    newPasswordHash = generate_password_hash(newPassword)

    student.password = newPassword
    student.passwordHash = newPasswordHash
    student.save()

    msg = u'{}的密码已经重置为：{}'.format(student.chineseName, newPassword)
    flash(msg, 'success')
    return redirect(url_for('bpCourse.roster', courseId=course.id))



