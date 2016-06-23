# -*- coding: utf-8 -*-

import math
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import User, Course
from ..constants import CntPermission
from ..utilities import Paginator, permission_required
from . import bpCourse


@bpCourse.route('/taught', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def taught():
    me = current_user

    currentPage = request.args.get('currentPage', 1, type=int)
    numOfCourses = (Course
                    .select()
                    .where(Course.teacher == me.id)
                    .count())
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfCourses) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfCourses, current=currentPage, per_page=numOfPerPage)

    if numOfCourses <= 0:
        return render_template('course/teacher/taught.html', pagination=pagination,
                               courses=[])
    query = (Course
             .where(Course.teacher == me.id)
             .order_by(Course.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    courses = [row for row in query]
    return render_template('course/teacher/taught.html', pagination=pagination,
                           courses=courses)




