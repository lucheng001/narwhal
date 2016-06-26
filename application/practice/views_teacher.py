# -*- coding: utf-8 -*-

import os
import math
import datetime
import shutil
from urllib.parse import quote
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, request, abort, send_from_directory
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import Practice
from ..constants import CntPermission, CntDepartment, CntSyllabusYear, CntPracticeMaterials
from ..utilities import Paginator, permission_required
from .forms_teacher import UploadMaterialsForm
from . import bpPractice

_all_ = ['taught', 'uploadMaterials', 'downloadMaterials', 'archivePractice']


@bpPractice.route('/taught', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def taught():
    me = current_user

    query = (Practice
             .select(Practice.semester)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = me.id
    currentDepartment = request.args.get('currentDepartment', 'all')
    currentSemester = request.args.get('currentSemester', 'all')
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Practice.teacher == currentTeacher)
    condition2 = (Practice.semester == currentSemester) if currentSemester in semesterLabels else None
    condition3 = (Practice.department == currentDepartment) if currentDepartment in CntDepartment.labels else None
    condition4 = (Practice.syllabusYear == currentSyllabusYear) if currentSyllabusYear in CntSyllabusYear.labels else None

    conditionArray1 = [condition1, condition2, condition3, condition4]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Practice.select()
    query = query.where(conditions) if conditions is not None else query
    numOfPractices = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfPractices) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfPractices, current=currentPage, per_page=numOfPerPage)

    if numOfPractices <= 0:
        return render_template('Practice/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                               currentDepartment=currentDepartment, currentTeacher=currentTeacher,
                               currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                               practices=[], semesters=semesters)

    query = (Practice
             .select()
             .order_by(Practice.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    practices = [row for row in query]
    return render_template('practice/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                           currentDepartment=currentDepartment, currentTeacher=currentTeacher,
                           currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                           practices=practices, semesters=semesters)


@bpPractice.route('/upload/materials/<category>/<int:practiceId>/', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.NORMAL)
def uploadMaterials(category, practiceId):
    practice = get_object_or_404(Practice, (Practice.id == practiceId))
    me = current_user
    if practice.teacher_id != me.id:
        abort(403)

    if category not in CntPracticeMaterials.labels:
        abort(404)

    filePath = os.path.join(current_app.config['APP_PRACTICE_FOLDER'],
                            practice.getFolderPath(me.chineseName))

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
        oldFileInfo = getattr(practice, category)
        if oldFileInfo is None:
            newFileInfo = u'{:02d}|{}'.format(1, fExtension)
        else:
            idx, _ = oldFileInfo.split(u'|')
            idx1 = int(idx) + 1
            newFileInfo = u'{:02d}|{}'.format(idx1, fExtension)

        pattern = practice.getMaterialNamePattern(category)
        fileName = pattern.format(idx=idx1, ext=fExtension)
        form.materials.data.save(os.path.join(filePath, fileName))

        tplFileName = practice.getTplMaterialName(category)
        if os.path.isfile(os.path.join(filePath, tplFileName)):
            os.remove(os.path.join(filePath, tplFileName))

        params = dict(zip([category], [newFileInfo]))
        query = Practice.update(**params).where(Practice.id == practice.id)
        query.execute()

        flash(u'资料上传成功', 'success')
        return redirect(url_for('.taught'))

    return render_template('practice/teacher/uploadMaterials.html', form=form,
                           practice=practice, category=category)


@bpPractice.route('/download/materials/<category>/<int:practiceId>/', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def downloadMaterials(category, practiceId):
    practice = get_object_or_404(Practice, (Practice.id == practiceId))
    teacher = practice.teacher
    me = current_user

    if category not in CntPracticeMaterials.labels:
        abort(404)

    canDownload = False
    if practice.teacher_id == me.id:
        canDownload = True
    elif me.hasPermission(CntPermission.COLLEGE):
        canDownload = True
    elif me.hasPermission(CntPermission.DEPARTMENT) and CntDepartment.isDirector(practice.department, me.userName):
        canDownload = True
    else:
        canDownload = False

    idx1 = 0
    ext = u'unknown'
    fileInfo = getattr(practice, category)
    if fileInfo is None:
        abort(404)
    else:
        idx, ext = fileInfo.split(u'|')
        idx1 = int(idx)

    pattern = practice.getMaterialNamePattern(category)
    fileName = pattern.format(idx=idx1, ext=ext)
    encodeFileName = quote(fileName.encode('UTF-8'))
    filePath = os.path.join(current_app.config['APP_PRACTICE_FOLDER'],
                            practice.getFolderPath(teacher.chineseName))

    return send_from_directory(filePath, fileName,
                               as_attachment=True,
                               attachment_filename=encodeFileName)


@bpPractice.route('/archive/<int:practiceId>/', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.NORMAL)
def archivePractice(practiceId):
    practice = get_object_or_404(Practice, (Practice.id == practiceId))
    teacher = practice.teacher
    me = current_user

    canDownload = False
    if Practice.teacher_id == me.id:
        canDownload = True
    elif me.hasPermission(CntPermission.COLLEGE):
        canDownload = True
    elif me.hasPermission(CntPermission.DEPARTMENT) and CntDepartment.isDirector(practice.department, me.userName):
        canDownload = True
    else:
        canDownload = False

    fileString = practice.getFolder(teacher.chineseName)
    filePath = os.path.join(current_app.config['APP_PRACTICE_FOLDER'],
                            practice.getFolderPath(teacher.chineseName))

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


