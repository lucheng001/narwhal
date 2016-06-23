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
            return render_template('course/course/../templates/course/college/badData.html', badData=badData)
        else:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'success')
            return redirect(url_for('.all'))

    return render_template('course/course/addByBatch.html', form=form)




