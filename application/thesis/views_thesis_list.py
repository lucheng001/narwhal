# -*- coding: utf-8 -*-


import os
import math
import datetime
import shutil
from flask import  render_template, request, current_app, send_from_directory, abort, flash, redirect
from flask_login import  login_required, current_user
from playhouse.flask_utils import get_object_or_404
from urllib.parse import quote
from ..constants import CntThesisMaterials, CntDepartment, CntPermission
from ..utilities import Paginator, permission_required
from ..models import Thesis, User
from . import  bpThesis
from .forms_upload_data import UploadMaterialsForm

_all_ = ['taught', 'departmentThesisList', 'archiveThesis']

@bpThesis.route('/taught', methods = ['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def taught():
    me = current_user

    query = (Thesis.select(Thesis.semester).distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = me.id
    currentSemester = request.args.get('currentSemester', 'all')

    condition1 = (Thesis.teacher == currentTeacher)
    condition2 = (Thesis.semester == currentSemester) if currentSemester in semesterLabels else None

    conditionArray1 = [condition1, condition2]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Thesis.select()
    query = query.where(conditions) if conditions is not None else query
    numOfThesis = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfThesis) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfThesis, current=currentPage, per_page=numOfPerPage)

    if numOfThesis <= 0:
        return render_template('thesis/showThesis/taught.html', pagination=pagination, currentPage=currentPage,
                               currentTeacher=currentTeacher,currentSemester=currentSemester,
                               thesiss=[], semesters=semesters)

    query = (Thesis
             .select()
             .order_by(Thesis.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    thesiss = [row for row in query]
    return render_template('thesis/showThesis/taught.html', pagination=pagination, currentPage=currentPage,
                           currentTeacher=currentTeacher, currentSemester=currentSemester,
                           thesiss=thesiss, semesters=semesters)



@bpThesis.route('/department', methods=['GET'])
@login_required
@permission_required(CntPermission.DEPARTMENT)
def departmentThesisList():
    me = current_user
    department = CntDepartment.witchDepartment(me.userName)
    if department not in CntDepartment.labels:
        abort(404)

    if not CntDepartment.isDirector(department, me.userName):
        abort(403)

    query = (User
             .select(User.id, User.chineseName)
             .join(Thesis)
             .where(Thesis.department == department)
             .distinct())
    teachers = [row for row in query]
    teacherIds = [teacher.id for teacher in teachers]

    query = (Thesis
             .select(Thesis.semester)
             .where(Thesis.department == department)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = request.args.get('currentTeacher', 0, type=int)
    currentDepartment = department
    currentSemester = request.args.get('currentSemester', 'all')

    condition1 = (Thesis.teacher == currentTeacher) if currentTeacher in teacherIds else None
    condition2 = (Thesis.semester == currentSemester) if currentSemester in semesterLabels else None
    condition3 = (Thesis.department == department)

    conditionArray1 = [condition1, condition2, condition3]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Thesis.select()
    query = query.where(conditions) if conditions is not None else query
    numOfThesis = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfThesis) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfThesis, current=currentPage, per_page=numOfPerPage)

    if numOfThesis <=0:
        return render_template('thesis/showThesis/departmentThesisList.html', pagination=pagination, currentPage=currentPage,
                               currentTeacher=currentTeacher, currentDepartment=currentDepartment, currentSemester=currentSemester,
                               thesis=[], teachers=teachers, semesters=semesters)

    query = (Thesis
             .select()
             .order_by(Thesis.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    thesiss = [row for row in query]
    return render_template('thesis/showThesis/departmentThesisList.html', pagination=pagination, currentPage=currentPage,
                               currentTeacher=currentTeacher, currentDepartment=department, currentSemester=currentSemester,
                               thesiss=thesiss, teachers=teachers, semesters=semesters)


@bpThesis.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.COLLEGE)
def all():
    me = current_user

    query = (User
             .select(User.id, User.chineseName)
             .order_by(User.userName.asc()))
    teachers = [row for row in query]
    teacherIds = [teacher.id for teacher in teachers]

    query = (Thesis
             .select(Thesis.semester)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = request.args.get('currentTeacher', 0, type=int)
    currentDepartment = request.args.get('currentDepartment', 'all')
    currentSemester = request.args.get('currentSemester', 'all')

    condition1 = (Thesis.teacher == currentTeacher) if currentTeacher in teacherIds else None
    condition2 = (Thesis.semester == currentSemester) if currentSemester in semesterLabels else None
    condition3 = (Thesis.department == currentDepartment) if currentDepartment in CntDepartment.labels else None

    conditionArray1 = [condition1, condition2, condition3]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Thesis.select()
    query = query.where(conditions) if conditions is not None else query
    numOfThesis = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfThesis) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfThesis, current=currentPage, per_page=numOfPerPage)

    if numOfThesis <= 0:
        return render_template('thesis/showThesis/allThesis.html', pagination=pagination,
                               currentPage=currentPage,
                               currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                               currentSemester=currentSemester,
                               thesis=[], teachers=teachers, semesters=semesters)

    query = (Thesis
             .select()
             .order_by(Thesis.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    thesiss = [row for row in query]
    return render_template('thesis/showThesis/allThesis.html', pagination=pagination,
                           currentPage=currentPage,
                           currentTeacher=currentTeacher, currentDepartment=currentDepartment,
                           currentSemester=currentSemester,
                           thesiss=thesiss, teachers=teachers, semesters=semesters)



@bpThesis.route('/archiveThesis/<int:thesisId>', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.NORMAL)
def archiveThesis(thesisId):
    thesis = get_object_or_404(Thesis, (Thesis.id == thesisId))
    teacher = thesis.teacher
    me = current_user

    canDownload = False
    if me.id == thesis.teacher_id:
        canDownload =True
    elif me.hasPermission(CntPermission.COLLEGE):
        canDownload = True
    elif me.hasPermission(CntPermission.DEPARTMENT) and CntDepartment.isDirector(thesis.department, me.userName):
        canDownload = True
    else:
        canDownload = False

    fileString = thesis.getFolder(thesis.studentName)
    filePath = os.path.join(current_app.config['APP_THESIS_FOLDER'],
                            thesis.getFolderPath(teacher.chineseName))
    timeString = u'{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    archiveName = u'{}_{}'.format(timeString, fileString)
    archivePath = os.path.join(current_app.config['APP_ARCHIVE_FOLDER'], archiveName)
    shutil.make_archive(archivePath, 'zip', filePath)

    zipName = u'{}.zip'.format(archiveName)
    encodeZipName = quote(zipName.encode('UTF-8'))
    zipPath = current_app.config['APP_ARCHIVE_FOLDER']

    return send_from_directory(zipPath, zipName,
                               as_attachment=True,
                               attachment_filename=encodeZipName)




