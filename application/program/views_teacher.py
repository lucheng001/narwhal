# -*- coding: utf-8 -*-

import os
import math
import datetime
import shutil
from urllib.parse import quote
from flask import render_template, current_app, request, abort, send_from_directory
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import Program
from ..constants import CntPermission, CntDepartment, CntSyllabusYear, CntProgramMaterials
from ..utilities import Paginator, permission_required
from . import bpProgram

_all_ = ['taught', 'downloadMaterials']


@bpProgram.route('/taught', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def taught():
    me = current_user

    currentPage = request.args.get('currentPage', 1, type=int)
    currentDepartment = request.args.get('currentDepartment', 'all')
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Program.department == currentDepartment) if currentDepartment in CntDepartment.labels else None
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
        return render_template('program/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                               currentDepartment=currentDepartment, currentSyllabusYear=currentSyllabusYear,
                               programs=[])

    query = (Program
             .select()
             .order_by(Program.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    programs = [row for row in query]
    return render_template('program/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                           currentDepartment=currentDepartment, currentSyllabusYear=currentSyllabusYear,
                           programs=programs)


@bpProgram.route('/download/materials/<category>/<int:programId>', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def downloadMaterials(category, programId):
    program = get_object_or_404(Program, (Program.id == programId))

    if category not in CntProgramMaterials.labels:
        abort(404)

    idx1 = 0
    ext = u'unknown'
    fileInfo = getattr(program, category)
    if fileInfo is None:
        abort(404)
    else:
        idx, ext = fileInfo.split(u'|')
        idx1 = int(idx)

    pattern = program.getMaterialNamePattern(category)
    fileName = pattern.format(idx=idx1, ext=ext)
    encodeFileName = quote(fileName.encode('UTF-8'))
    filePath = os.path.join(current_app.config['APP_PROGRAM_FOLDER'], program.getFolderPath())

    return send_from_directory(filePath, fileName,
                               as_attachment=True,
                               attachment_filename=encodeFileName)




