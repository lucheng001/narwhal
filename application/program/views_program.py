# -*- coding: utf-8 -*-

import os
import re
import datetime
import shutil
from flask import render_template, redirect, url_for, flash, current_app, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import login_required, current_user
from ..models import Program
from ..constants import CntPermission, CntDepartment
from ..utilities import permission_required
from .forms_program import AddProgramForm, AddProgramDataForm
from . import bpProgram

_all_ = ['addByBatch', 'delete']


@bpProgram.route('/add/batch', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.PROGRAM)
def addByBatch():
    form = AddProgramDataForm()
    if form.validate_on_submit():
        lines = form.programData.data.splitlines()
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
            data5 = [re.sub(u'[-]', u'', d) for d in data4]
            data = [re.sub(u'[_]', u'', d) for d in data5]
            name, theory, laboratory, practice, departmentName, syllabusYear = data

            departmentLable = u''
            for department in CntDepartment.choices:
                if departmentName == department[1]:
                    departmentLable = department[0]
                    break
            else:
                badData.append(line)
                continue

            programDict = dict(
                name=name,
                theory=int(theory),
                laboratory=int(laboratory),
                practice=round(float(practice), 1),
                department=departmentLable,
                syllabusYear=syllabusYear
            )

            programForm = AddProgramForm()

            programForm.theory.raw_data = [theory]
            programForm.laboratory.raw_data = [laboratory]
            programForm.practice.raw_data = [practice]

            programForm.name.data = programDict['name']
            programForm.theory.data = programDict['theory']
            programForm.laboratory.data = programDict['laboratory']
            programForm.practice.data = programDict['practice']
            programForm.syllabusYear.data = programDict['syllabusYear']
            programForm.department.data = programDict['department']

            if not programForm.validate():
                badData.append(line)
                continue

            p = u'{name}-{theory:03d}+{laboratory:03d}+{practice:.1f}'
            filePath = os.path.join(current_app.config['APP_PROGRAM_FOLDER'],
                                    syllabusYear, departmentName,
                                    p.format(**programDict))
            if os.path.isdir(filePath):
                badData.append(line)
                continue

            # os.makedirs(filePath)
            tplPath = current_app.config['APP_PROGRAM_TPL']
            shutil.copytree(tplPath, filePath)

            Program.create(**programDict)

            goodData.append(line)

        msg = (u'共提交数据<span class="badge badge-primary"> {} </span>条，'
               u'添加成功<span class="badge badge-success"> {} </span>条，'
               u'添加失败<span class="badge badge-danger"> {} </span>条')
        if badData:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'error')
            return render_template('program/program/badData.html', badData=badData)
        else:
            flash(msg.format(len(lines), len(goodData), len(badData)), 'success')
            if current_user.hasPermission(CntPermission.COLLEGE):
                return redirect(url_for('.all'))
            elif current_user.hasPermission(CntPermission.DEPARTMENT):
                return redirect(url_for('.tasks'))
            else:
                abort(403)

    return render_template('program/program/addByBatch.html', form=form)


@bpProgram.route('/delete/<int:programId>/', methods=['GET'])
@login_required
@permission_required(CntPermission.PROGRAM)
def delete(programId):
    program = get_object_or_404(Program, (Program.id == programId))

    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    fileString = program.getFolder()
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileString))
    filePath = os.path.join(current_app.config['APP_PROGRAM_FOLDER'], program.getFolderPath())

    # if os.path.isdir(filePath):
    #     shutil.rmtree(filePath)

    shutil.move(filePath, recyclePath)

    program.delete_instance()

    flash(u'删除成功', 'success')
    return redirect(url_for('.all'))


