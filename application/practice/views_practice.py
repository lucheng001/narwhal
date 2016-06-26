# -*- coding: utf-8 -*-

import os
import re
import datetime
import shutil
from flask import render_template, redirect, url_for, flash, current_app
from playhouse.flask_utils import get_object_or_404
from flask_login import login_required
from ..models import User, Practice
from ..constants import CntPermission, CntDepartment
from ..utilities import permission_required
from .forms_practice import AddPracticeForm, AddPracticeDataForm
from . import bpPractice

_all_ = ['addByBatch', 'all', 'delete']


@bpPractice.route('/add/batch', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.PRACTICE)
def addByBatch():
    form = AddPracticeDataForm()
    if form.validate_on_submit():
        query = (User
                 .select(User.id, User.chineseName))
        teachers = [row for row in query]

        lines = form.practiceData.data.splitlines()
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

            practiceDict = dict(
                name=name,
                teacherName=teacherName,
                teacher=teacherId,
                klass=klass,
                semester=semester,
                departmentName=departmentName,
                department=departmentLable,
                syllabusYear=syllabusYear
            )

            practiceForm = AddPracticeForm()
            practiceForm.teacher.choices = [(teacher.id, teacher.chineseName) for teacher in teachers]
            practiceForm.name.data = practiceDict['name']
            practiceForm.teacher.data = practiceDict['teacher']
            practiceForm.klass.data = practiceDict['klass']
            practiceForm.semester.data = practiceDict['semester']
            practiceForm.department.data = practiceDict['department']
            practiceForm.syllabusYear.data = practiceDict['syllabusYear']

            if not practiceForm.validate():
                badData.append(line)
                continue

            p = u'{teacherName}-{name}-{klass}'
            filePath = os.path.join(current_app.config['APP_PRACTICE_FOLDER'],
                                    semester, departmentName,
                                    p.format(**practiceDict))
            if os.path.isdir(filePath):
                badData.append(line)
                continue

            # os.makedirs(filePath)
            tplPath = current_app.config['APP_PRACTICE_TPL']
            shutil.copytree(tplPath, filePath)

            Practice.create(**practiceDict)

            goodData.append(line)

        msg = (u'共提交数据<span class="badge badge-primary">{}</span>条，'
               u'添加成功<span class="badge badge-success">{}</span>条，'
               u'失败添加<span class="badge badge-danger">{}</span>条')
        if badData:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'error')
            return render_template('practice/practice/badData.html', badData=badData)
        else:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'success')
            return redirect(url_for('.all'))

    return render_template('practice/practice/addByBatch.html', form=form)


@bpPractice.route('/delete/<int:practiceId>/', methods=['GET'])
@login_required
@permission_required(CntPermission.PRACTICE)
def delete(practiceId):
    practice = get_object_or_404(Practice, (Practice.id == practiceId))
    teacher = practice.teacher

    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    fileString = practice.getFolder(teacher.chineseName)
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileString))
    filePath = os.path.join(current_app.config['APP_PRACTICE_FOLDER'],
                            practice.getFolderPath(teacher.chineseName))

    # if os.path.isdir(filePath):
    #     shutil.rmtree(filePath)

    shutil.move(filePath, recyclePath)

    practice.delete_instance()

    flash(u'删除成功', 'success')
    return redirect(url_for('.all'))


