# -*- coding: utf-8 -*-

import os
import re
import shutil
from flask import render_template, redirect, url_for, flash, current_app
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import User, Course
from ..constants import CntPermission, CntDepartment, CntSyllabusYear
from ..utilities import permission_required
from .forms_course import AddCourseForm, AddCourseDataForm
from . import bpCourse

_all_ = ['addByBatch', 'all', 'delete']


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
        for line in lines:
            data1 = line.split(',')
            if len(data1) != 6:
                badData.append(line)
                continue

            data2 = [re.sub('[\s+]', '', d) for d in data1]
            data = [re.sub('[()]', '', d) for d in data2]
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

            if not courseForm.validate():
                badData.append(line)
                continue

            filePath = os.path.join(current_app.config['APP_COURSE_FOLDER'],
                                    semester, departmentName,
                                    u'{}-{}-{}'.format(teacherName, name, klass))
            if os.path.isdir(filePath):
                badData.append(line)
                continue

            # os.makedirs(filePath)
            tplPath = current_app.config['APP_COURSE_TPL']
            shutil.copytree(tplPath, filePath)

            Course.create(**courseDict)

            goodData.append(line)

        msg = (u'共提交数据<span class="badge badge-primary">{}</span>条，'
               u'添加成功<span class="badge badge-success">{}</span>条，'
               u'失败添加<span class="badge badge-danger">{}</span>条')
        if badData:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'error')
            return render_template('course/course/badData.html', badData=badData)
        else:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'success')
            return redirect(url_for('.all'))

    return render_template('course/course/addByBatch.html', form=form)


@bpCourse.route('/delete/<int:courseId>/', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def delete(courseId):
    course = get_object_or_404(Course, (Course.id == courseId))
    teacher = course.teacher

    import datetime
    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    fileString = u'{}-{}-{}'.format(teacher.chineseName, course.name, course.klass)
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileString))
    filePath = os.path.join(current_app.config['APP_COURSE_FOLDER'],
                            course.semester, course.getDepartmentName(),
                            fileString)

    # if os.path.isdir(filePath):
    #     shutil.rmtree(filePath)

    shutil.copytree(filePath, recyclePath)

    course.delete_instance()

    flash(u'删除成功', 'success')
    return redirect(url_for('.all'))


