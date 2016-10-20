
import os
import math
import datetime
import shutil
from . import  bpThesis
from urllib.parse import quote
from flask import  render_template, request, current_app, send_from_directory, abort, flash, redirect
from flask_login import  login_required, current_user
from ..constants import CntThesisMaterials
from playhouse.flask_utils import get_object_or_404
from ..utilities import Paginator
from ..models import Thesis
from .forms_upload_data import UploadMaterialsForm

_all_ = ['taught']

@bpThesis.route('/taught', methods = ['GET'])
@login_required
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


@bpThesis.route('/archiveThesis/<int:thesisId>', methods=['GET', 'POST'])
@login_required
def archiveThesis(thesisId):
    thesis = get_object_or_404(Thesis, (Thesis.id == thesisId))
    teacher = thesis.teacher
    me = current_user

    canDownload = False
    if me.id == thesis.teacher_id:
        canDownload =True

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




