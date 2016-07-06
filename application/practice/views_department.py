# -*- coding: utf-8 -*-

import math
from flask import render_template, current_app, request, abort
from flask_login import current_user, login_required
from ..models import User, Practice
from ..constants import CntPermission, CntDepartment, CntSyllabusYear
from ..utilities import Paginator, permission_required
from . import bpPractice

_all_ = ['tasks']


@bpPractice.route('/tasks', methods=['GET'])
@login_required
@permission_required(CntPermission.DEPARTMENT)
def tasks():
    me = current_user

    department = CntDepartment.witchDepartment(me.userName)
    if department not in CntDepartment.labels:
        abort(404)

    if not CntDepartment.isDirector(department, me.userName):
        abort(403)

    query = (User
             .select(User.id, User.chineseName)
             .join(Practice)
             .where(Practice.department == department)
             .order_by(User.userName.asc())
             .distinct())
    teachers = [row for row in query]
    teacherIds = [teacher.id for teacher in teachers]

    query = (Practice
             .select(Practice.semester)
             .where(Practice.department == department)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = request.args.get('currentTeacher', 0, type=int)
    currentDepartment = department
    currentSemester = request.args.get('currentSemester', 'all')
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Practice.teacher == currentTeacher) if currentTeacher in teacherIds else None
    condition2 = (Practice.semester == currentSemester) if currentSemester in semesterLabels else None
    condition3 = (Practice.department == currentDepartment)
    condition4 = (Practice.syllabusYear == currentSyllabusYear) if currentSyllabusYear in CntSyllabusYear.labels else None

    conditionArray1 = [condition1, condition2, condition3, condition4]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Practice.select()
    query = query.where(conditions) if conditions is not None else query
    numOfPractices = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfPractices) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfPractices, current=currentPage, per_page=numOfPerPage)

    if numOfPractices <= 0:
        return render_template('practice/department/tasks.html', pagination=pagination, currentPage=currentPage,
                               currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                               currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                               practices=[], teachers=teachers, semesters=semesters)

    query = (Practice
             .select(Practice, User.chineseName)
             .join(User)
             .order_by(Practice.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    practices = [row for row in query]
    return render_template('practice/department/tasks.html', pagination=pagination, currentPage=currentPage,
                           currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                           currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                           practices=practices, teachers=teachers, semesters=semesters)


