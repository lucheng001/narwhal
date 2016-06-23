# -*- coding: utf-8 -*-

import math
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import User, Course
from ..constants import CntPermission, CntDepartment, CntSyllabusYear
from ..utilities import Paginator, permission_required
from . import bpCourse

_all_ = ['taught']


@bpCourse.route('/taught', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def taught():
    me = current_user

    query = (Course
             .select(Course.semester)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = me.id
    currentDepartment = request.args.get('currentDepartment', 'all')
    currentSemester = request.args.get('currentSemester', 'all')
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Course.teacher == currentTeacher)
    condition2 = (Course.semester == currentSemester) if currentSemester in semesterLabels else None
    condition3 = (Course.department == currentDepartment) if currentDepartment in CntDepartment.labels else None
    condition4 = (Course.syllabusYear == currentSyllabusYear) if currentSyllabusYear in CntSyllabusYear.labels else None

    conditionArray1 = [condition1, condition2, condition3, condition4]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Course.select()
    query = query.where(conditions) if conditions is not None else query
    numOfCourses = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfCourses) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfCourses, current=currentPage, per_page=numOfPerPage)

    if numOfCourses <= 0:
        return render_template('course/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                               currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                               currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                               courses=[], semesters=semesters)

    query = (Course
             .select()
             .order_by(Course.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    courses = [row for row in query]
    return render_template('course/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                           currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                           currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                           courses=courses, semesters=semesters)




