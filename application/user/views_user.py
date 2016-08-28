# -*- coding: utf-8 -*-

import math
from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_required
from playhouse.flask_utils import get_object_or_404
from ..models import User, Course
from ..utilities import permission_required, generate_random_string, Paginator
from ..constants import CntGender, CntRoles, CntPermission
from .forms_user import AddUserForm
from . import bpUser

_all_ = ['all', 'add', 'resetPassword', 'delete']


@bpUser.route('/resetPassword/<int:userId>', methods=['GET'])
@login_required
@permission_required(CntPermission.USER)
def resetPassword(userId):
    user = get_object_or_404(User, (User.id == userId))
    from werkzeug.security import generate_password_hash
    newPassword = generate_random_string()
    newPasswordHash = generate_password_hash(newPassword)

    user.password = newPassword
    user.passwordHash = newPasswordHash
    user.save()

    msg = (u'<span class="label label-primary">{}</span> '
           u'的密码已经重置为：'
           u'<span class="label label-danger">{}</span>')
    flash(msg.format(user.chineseName, newPassword), 'success')
    return redirect(url_for('.all'))


@bpUser.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.USER)
def all():
    me = current_user

    currentPage = request.args.get('currentPage', 1, type=int)
    currentGender = request.args.get('currentGender', 'all')
    currentRole = request.args.get('currentRole', 'all')

    condition1 = (User.gender == currentGender) if currentGender in CntGender.labels else None
    condition2 = (User.role == currentRole) if currentRole in CntRoles.labels else None

    conditionArray1 = [condition1, condition2]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = User.select()
    query = query.where(conditions) if conditions is not None else query
    numOfUsers = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfUsers) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfUsers, current=currentPage, per_page=numOfPerPage)

    if numOfUsers <= 0:
        return render_template('user/user/all.html', pagination=pagination, currentPage=currentPage,
                               currentGender=currentGender, currentRole=currentRole,
                               users=[])

    query = (User
             .select(
                User.id,
                User.userName,
                User.chineseName,
                User.gender,
                User.role)
             .order_by(User.userName.asc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    users = [row for row in query]
    return render_template('user/user/all.html', pagination=pagination, currentPage=currentPage,
                           currentGender=currentGender, currentRole=currentRole,
                           users=users)


@bpUser.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.USER)
def add():
    form = AddUserForm()

    if form.validate_on_submit():
        import re
        from werkzeug.security import generate_password_hash
        User.create(
            userName=re.sub('[\s+]', '', form.userName.data),
            chineseName=re.sub('[\s+]', '', form.chineseName.data),
            gender=form.gender.data,
            role=form.role.data,
            permission=CntRoles.getRolePermission(form.role.data),
            password=form.password.data,
            passwordHash=generate_password_hash(form.password.data)
        )
        flash(u'添加成功', 'success')
        return redirect(url_for('.all'))

    return render_template('user/user/add.html', form=form)


@bpUser.route('/delete/<int:userId>', methods=['GET'])
@login_required
@permission_required(CntPermission.USER)
def delete(userId):
    user = get_object_or_404(User, (User.id == userId))

    numOfCourses = (Course
                    .select()
                    .where(Course.teacher == user.id)
                    .count())
    if numOfCourses == 0:
        user.delete_instance()
        flash(u'删除成功', 'success')
    else:
        flash(u'删除失败，用户存在课程数据', 'error')

    return redirect(url_for('.all'))


