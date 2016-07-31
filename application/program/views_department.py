# -*- coding: utf-8 -*-

import os
import math
from werkzeug.utils import secure_filename
from flask import render_template, current_app, abort, flash, redirect, url_for, request
from flask_login import current_user, login_required
from playhouse.flask_utils import get_object_or_404
from ..models import Program
from ..constants import CntPermission, CntDepartment, CntSyllabusYear, CntProgramMaterials
from ..utilities import permission_required, Paginator
from .forms_department import UploadMaterialsForm
from . import bpProgram

_all_ = ['tasks', 'uploadMaterials']


@bpProgram.route('/tasks', methods=['GET'])
@login_required
@permission_required(CntPermission.DEPARTMENT)
def tasks():
    me = current_user

    department = CntDepartment.witchDepartment(me.userName)
    if department not in CntDepartment.labels:
        abort(404)

    if not CntDepartment.isDirector(department, me.userName):
        abort(403)

    currentPage = request.args.get('currentPage', 1, type=int)
    currentDepartment = department
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Program.department == department)
    condition2 = (Program.syllabusYear == currentSyllabusYear) if currentSyllabusYear in CntSyllabusYear.labels else None

    conditionArray1 = [condition1, condition2]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Program.select()
    query = query.where(conditions) if conditions is not None else query
    numOfPrograms = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfPrograms) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfPrograms, current=currentPage, per_page=numOfPerPage)

    if numOfPrograms <= 0:
        return render_template('program/department/tasks.html', pagination=pagination, currentPage=currentPage,
                               currentDepartment=currentDepartment, currentSyllabusYear=currentSyllabusYear,
                               programs=[])

    query = (Program
             .select()
             .order_by(Program.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    programs = [row for row in query]
    return render_template('program/department/tasks.html', pagination=pagination, currentPage=currentPage,
                           currentDepartment=currentDepartment, currentSyllabusYear=currentSyllabusYear,
                           programs=programs)


@bpProgram.route('/upload/materials/<category>/<int:programId>', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.DEPARTMENT)
def uploadMaterials(category, programId):
    program = get_object_or_404(Program, (Program.id == programId))

    if category not in CntProgramMaterials.labels:
        abort(404)

    me = current_user
    department = CntDepartment.witchDepartment(me.userName)
    if department not in CntDepartment.labels:
        abort(404)

    if not CntDepartment.isDirector(department, me.userName):
        abort(403)

    if program.department != department:
        abort(403)

    filePath = os.path.join(current_app.config['APP_PROGRAM_FOLDER'], program.getFolderPath())

    form = UploadMaterialsForm()
    if form.validate_on_submit():
        fName = u'untitled'
        fExtension = u'unknown'
        secureFileName = secure_filename(form.materials.data.filename)
        if secureFileName:
            res = secureFileName.rsplit('.', 1)
            if len(res) == 2:
                fName, fExtension = res[0], res[1]
            else:
                fName, fExtension = '', res[0]

        newFileInfo = None
        idx1 = 1
        oldFileInfo = getattr(program, category)
        if oldFileInfo is None:
            newFileInfo = u'{:02d}|{}'.format(1, fExtension)
        else:
            idx, _ = oldFileInfo.split(u'|')
            idx1 = int(idx) + 1
            newFileInfo = u'{:02d}|{}'.format(idx1, fExtension)

        pattern = program.getMaterialNamePattern(category)
        fileName = pattern.format(idx=idx1, ext=fExtension)

        form.materials.data.save(os.path.join(filePath, fileName))

        tplFileName = program.getTplMaterialName(category)
        if os.path.isfile(os.path.join(filePath, tplFileName)):
            os.remove(os.path.join(filePath, tplFileName))

        params = dict(zip([category], [newFileInfo]))
        query = Program.update(**params).where(Program.id == program.id)
        query.execute()

        flash(u'资料上传成功', 'success')
        return redirect(url_for('.tasks'))

    return render_template('program/department/uploadMaterials.html', form=form,
                           program=program, category=category)




