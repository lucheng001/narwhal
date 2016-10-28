# -*- coding: utf-8 -*-

import re
import os
import shutil
from flask_login import login_required, current_user
from flask import render_template, current_app, flash, redirect, url_for
from ..models import User, Thesis
from ..constants import CntDepartment, CntPermission
from ..utilities import permission_required
from .forms_add_student import AddStudentForm, AddStudentDataForm
from . import bpThesis

_all_ = ['addByBatch']

@bpThesis.route('/add/batch', methods=['POST', 'GET'])
@login_required
@permission_required(CntPermission.THESIS)
def addByBatch():
    form = AddStudentDataForm()
    if form.validate_on_submit():
        query = (User.select(User.id, User.chineseName, User.userName))
        teachers = [row for row in query]
        me = current_user

        lines = form.studentData.data.splitlines()
        badData = []
        goodData = []

        for line in lines:
            data1 = line.split(',')
            if len(data1) != 6:
                badData.append(line)
                continue

            data2 = [re.sub(u'[\s+]', u'', d) for d in data1]
            data3 = [re.sub(u'[()]', u'', d) for d in data2]
            data4 = [re.sub(u'[（）]', u'', d) for d in data3]
            data = [re.sub(u'[_]', u'', d) for d in data4]
            stuNum, stuName, name, teacherName, semester, departmentName = data

            teacherID = 0
            for teacher in teachers:
                if teacherName == teacher.chineseName:
                    teacherID = teacher.id
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

            directorID = 0
            directorName = CntDepartment.getDepartmentDirectorName(departmentLable)
            for teacher in teachers:
                if directorName == teacher.userName:
                    directorID = teacher.id
                    break
            else:
                badData.append(line)
                continue

            thesisDic = dict(
                studentNum=stuNum,
                studentName=stuName,
                name=name,
                teacher=teacherID,
                reviewer=directorID,
                secretary=directorID,
                semester=semester,
                departmentName=departmentName,
                department=departmentLable
            )

            thesisForm = AddStudentForm()
            thesisForm.teacher.choices = [(teacher.id, teacher.chineseName) for teacher in teachers]
            thesisForm.teacher.data = thesisDic['teacher']
            thesisForm.studentNum.data = thesisDic['studentNum']
            thesisForm.studentName.data = thesisDic['studentName']
            thesisForm.name.data = thesisDic['name']
            thesisForm.semester.data = thesisDic['semester']
            thesisForm.department.data = thesisDic['department']

            if not thesisForm.validate():
                badData.append(line)
                continue




            p = u'{studentNum}{studentName}'
            filePath = os.path.join(current_app.config['APP_THESIS_FOLDER'],
                                    semester, departmentName, teacherName,
                                    p.format(**thesisDic))
            if os.path.isdir(filePath):
                badData.append(line)
                continue

            tplPath = current_app.config['APP_THESIE_TPL']
            shutil.copytree(tplPath, filePath)

            Thesis.create(**thesisDic)

            goodData.append(line)

        msg = (u'共提交数据<span class="badge badge-primary"> {} </span>条，'
               u'添加成功<span class="badge badge-success"> {} </span>条，'
               u'添加失败<span class="badge badge-danger"> {} </span>条')
        if badData:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'error')
            return render_template('thesis/teacher/badData.html', badData=badData)
        else:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'success')
            return redirect(url_for('bpThesis.addByBatch'))


    return render_template('thesis/teacher/addByBatch.html', form=form)