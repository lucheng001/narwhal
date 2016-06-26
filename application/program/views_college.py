# -*- coding: utf-8 -*-

import math
from flask import render_template, current_app, request
from flask_login import current_user, login_required
from ..models import Program
from ..constants import CntPermission, CntDepartment, CntSyllabusYear
from ..utilities import Paginator, permission_required
from . import bpProgram

_all_ = ['all']


@bpProgram.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.COLLEGE)
def all():
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
        return render_template('program/college/all.html', pagination=pagination, currentPage=currentPage,
                               currentDepartment=currentDepartment, currentSyllabusYear=currentSyllabusYear,
                               programs=[])

    query = (Program
             .select()
             .order_by(Program.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    programs = [row for row in query]
    return render_template('program/college/all.html', pagination=pagination, currentPage=currentPage,
                           currentDepartment=currentDepartment, currentSyllabusYear=currentSyllabusYear,
                           programs=programs)

