# -*- coding: utf-8 -*-

import math
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import User, Course
from ..constants import CntPermission, CntDepartment, CntSyllabusYear
from ..utilities import Paginator, permission_required
from .forms_course import AddCourseForm, AddCourseDataForm
from . import bpCourse

_all_ = ['addByBatch', 'all']


@bpCourse.route('/add/batch', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.COURSE)
def addByBatch():
    form = AddCourseDataForm()
    if form.validate_on_submit():
        query = (User
                 .select(User.id, User.chineseName))
        teachers = [row for row in query]

        lines = form.courseData.data.splitlines()
        badData = []
        goodData = []
        goodDict = []
        for line in lines:
            data = line.split(',')
            if len(data) != 6:
                badData.append(line)
                continue

            name, teacherName, klass, semester, departmentName, syllabusYear = data

            teacherId = 0
            for teacher in teachers:
                if teacherName == teacher.chineseName:
                    teacherId = teacher.id
                    break
            else:
                badData.append(line)
                continue

            departmentLable = u''
            for department in CntDepartment.choices:
                if departmentName == department[1]:
                    departmentLable = department[0]
                    break
            else:
                badData.append(line)
                continue

            courseDict = dict(
                name=name,
                teacher=teacherId,
                klass=klass,
                semester=semester,
                department=departmentLable,
                syllabusYear=syllabusYear
            )

            courseForm = AddCourseForm()
            courseForm.teacher.choices = [(teacher.id, teacher.chineseName) for teacher in teachers]
            courseForm.name.data = courseDict['name']
            courseForm.teacher.data = courseDict['teacher']
            courseForm.klass.data = courseDict['klass']
            courseForm.semester.data = courseDict['semester']
            courseForm.department.data = courseDict['department']
            courseForm.syllabusYear.data = courseDict['syllabusYear']

            if courseForm.validate():
                goodDict.append(courseDict)
                goodData.append(line)
            else:
                badData.append(line)

        from ..extensions import db
        with db.database.atomic():
            Course.insert_many(goodDict).execute()

        msg = u'共提交数据{}条，添加成功{}条，失败添加{}条'
        if badData:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'error')
            return render_template('course/course/badData.html', badData=badData)
        else:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'success')
            return redirect(url_for('.all'))

    return render_template('course/course/addByBatch.html', form=form)


@bpCourse.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.COURSE)
def all():
    me = current_user

    query = (User
             .select(User.id, User.chineseName))
    teachers = [row for row in query]
    teacherIds = [teacher.id for teacher in teachers]

    query = (Course
             .select(Course.semester)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = request.args.get('currentTeacher', 0, type=int)
    currentDepartment = request.args.get('currentDepartment', 'all')
    currentSemester = request.args.get('currentSemester', 'all')
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Course.teacher == currentTeacher) if currentTeacher in teacherIds else None
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
        return render_template('course/course/all.html', pagination=pagination, currentPage=currentPage,
                               currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                               currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                               courses=[], teachers=teachers, semesters=semesters)

    query = (Course
             .select(Course, User.chineseName)
             .join(User)
             .order_by(Course.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    courses = [row for row in query]
    return render_template('course/course/all.html', pagination=pagination, currentPage=currentPage,
                           currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                           currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                           courses=courses, teachers=teachers, semesters=semesters)

