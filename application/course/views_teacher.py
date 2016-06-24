# -*- coding: utf-8 -*-

import os
import math
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import Course
from ..constants import CntPermission, CntDepartment, CntSyllabusYear, CntCourseMaterials
from ..utilities import Paginator, permission_required
from .forms_teacher import UploadMaterialsForm
from . import bpCourse

_all_ = ['taught']


@bpCourse.route('/taught', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def taught():
    me = current_user

    query = (Course
             .select(Course.semester)
             .distinct())
    semesters = [row.semester for row in query]
    semesterLabels = [semester for semester in semesters]

    currentPage = request.args.get('currentPage', 1, type=int)
    currentTeacher = me.id
    currentDepartment = request.args.get('currentDepartment', 'all')
    currentSemester = request.args.get('currentSemester', 'all')
    currentSyllabusYear = request.args.get('currentSyllabusYear', 'all')

    condition1 = (Course.teacher == currentTeacher)
    condition2 = (Course.semester == currentSemester) if currentSemester in semesterLabels else None
    condition3 = (Course.department == currentDepartment) if currentDepartment in CntDepartment.labels else None
    condition4 = (Course.syllabusYear == currentSyllabusYear) if currentSyllabusYear in CntSyllabusYear.labels else None

    conditionArray1 = [condition1, condition2, condition3, condition4]
    conditionArray2 = [condition for condition in conditionArray1 if condition is not None]
    if conditionArray2:
        conditions = conditionArray2[0]
        for condition in conditionArray2[1:]:
            conditions &= condition
    else:
        conditions = None

    query = Course.select()
    query = query.where(conditions) if conditions is not None else query
    numOfCourses = query.count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfCourses) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfCourses, current=currentPage, per_page=numOfPerPage)

    if numOfCourses <= 0:
        return render_template('course/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                               currentDepartment=currentDepartment, currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                               courses=[], semesters=semesters)

    query = (Course
             .select()
             .order_by(Course.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    query = query.where(conditions) if conditions is not None else query
    courses = [row for row in query]
    return render_template('course/teacher/taught.html', pagination=pagination, currentPage=currentPage,
                           currentDepartment=currentDepartment, currentSemester=currentSemester, currentSyllabusYear=currentSyllabusYear,
                           courses=courses, semesters=semesters)


@bpCourse.route('/upload/materials/<category>/<int:courseId>/', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.NORMAL)
def uploadMaterials(category, courseId):
    course = get_object_or_404(Course, (Course.id == courseId))
    me = current_user
    if course.teacher_id != me.id:
        abort(403)

    if category not in CntCourseMaterials.labels:
        abort(404)

    filePath = os.path.join(current_app.config['APP_UPLOAD_FOLDER'],
                            course.semester, course.getDepartmentName(),
                            u'{}-{}'.format(me.chineseName, course.klass))

    form = UploadMaterialsForm()
    if form.validate_on_submit():
        fName = 'untitled'
        fExtension = 'unknown'
        secureFileName = secure_filename(form.materials.data.filename)
        if secureFileName:
            res = secureFileName.rsplit('.', 1)
            if len(res) == 2:
                fName, fExtension = res[0], res[1]
            else:
                fName, fExtension = '', res[0]

        fileName = u'{}.{}'.format(CntCourseMaterials.getMaterialName(category), fExtension)
        if os.path.isfile(os.path.join(filePath, fileName)):
            os.remove(os.path.join(filePath, fileName))

        oldFileName = getattr(course, category)
        if oldFileName and os.path.isfile(os.path.join(filePath, oldFileName)):
            os.remove(os.path.join(filePath, oldFileName))

        form.materials.data.save(os.path.join(filePath, fileName))

        tplFileName = u'{}.{}'.format(CntCourseMaterials.getMaterialName(category), u'未交')
        if os.path.isfile(os.path.join(filePath, tplFileName)):
            os.remove(os.path.join(filePath, tplFileName))

        params = dict(zip([category], [fileName]))
        query = Course.update(**params)
        query.execute()

        flash(u'资料上传成功', 'success')
        return redirect(url_for('.taught'))

    return render_template('course/teacher/uploadMaterials.html', form=form,
                           course=course, category=category)


