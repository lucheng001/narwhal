# -*- coding: utf-8 -*-

import math
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import User, Course, CourseStudent, Work, Sign
from ..constants import CntPermission
from ..utilities import Paginator, permission_required
from . import bpCourse


@bpCourse.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.STUDENT)
def all():
    currentPage = request.args.get('currentPage', 1, type=int)
    numOfCourses = (Course
                    .select()
                    .count())
    numOfPerPage = current_app.config['PT_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfCourses) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfCourses, current=currentPage, per_page=numOfPerPage)

    if numOfCourses <= 0:
        return render_template('course/student/all.html', pagination=pagination,
                               courses=[])

    query = (Course
             .select(Course, User.chineseName)
             .join(User)
             .order_by(Course.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    courses = [row for row in query]
    return render_template('course/student/all.html', pagination=pagination,
                           courses=courses)


@bpCourse.route('/take/<int:courseId>', methods=['GET'])
@login_required
@permission_required(CntPermission.STUDENT)
def take(courseId):
    course = get_object_or_404(Course, (Course.id == courseId))
    me = current_user

    if course.isEnd():
        flash(u'课程已经结束，无法加入', 'error')
        return redirect(url_for('.all'))

    query = (CourseStudent
             .select()
             .where(
                (CourseStudent.student == me.id) &
                (CourseStudent.course == course.id)))
    try:
        isExist = query.get()
    except CourseStudent.DoesNotExist:
        isExist = None
        CourseStudent.create(
            student=me._get_current_object(),
            course=course
        )
        flash(u'成功加入该课程', 'success')
        return redirect(url_for('.studied'))

    flash(u'已经加入该课程', 'warning')
    return redirect(url_for('.all'))


@bpCourse.route('/untake/<int:courseId>', methods=['GET'])
@login_required
@permission_required(CntPermission.STUDENT)
def untake(courseId):
    course = get_object_or_404(Course, (Course.id == courseId))
    me = current_user

    if course.isEnd():
        flash(u'课程已经结束，无法加入', 'error')
        return redirect(url_for('.all'))

    query = (CourseStudent
             .select()
             .where(
                (CourseStudent.student == me.id) &
                (CourseStudent.course == course.id)))
    try:
        isExist = query.get()
    except CourseStudent.DoesNotExist:
        isExist = None
        flash(u'未加入该课程', 'info')
        return redirect(url_for('.studied'))

    numOfWorks = (Work
                  .select()
                  .where(Work.student == me.id)
                  .count())
    if numOfWorks != 0:
        flash(u'已经上交该课程的作业，无法退出', 'error')
        return redirect(url_for('.studied'))

    numOfSigns = (Sign
                  .select()
                  .where(Sign.student == me.id)
                  .count())
    if numOfSigns != 0:
        flash(u'已经参加该课程的考勤，无法退出', 'error')
        return redirect(url_for('.studied'))

    query = (CourseStudent
             .delete()
             .where(
                (CourseStudent.student == me.id) &
                (CourseStudent.course == course.id)))
    query.execute()
    flash(u'已经成功退出该课程', 'success')
    return redirect(url_for('.studied'))


@bpCourse.route('/studied', methods=['GET'])
@login_required
@permission_required(CntPermission.STUDENT)
def studied():
    me = current_user

    currentPage = request.args.get('currentPage', 1, type=int)
    numOfCourses = (CourseStudent
                    .select()
                    .where(CourseStudent.student == me.id)
                    .count())
    numOfPerPage = current_app.config['PT_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfCourses) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfCourses, current=currentPage, per_page=numOfPerPage)

    if numOfCourses <= 0:
        return render_template('course/student/studied.html', pagination=pagination,
                               courses=[])

    query = (Course
             .select()
             .join(CourseStudent)
             .switch(Course)
             .join(User)
             .where(CourseStudent.student == me.id)
             .order_by(CourseStudent.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    courses = [row for row in query]

    return render_template('course/student/studied.html', pagination=pagination,
                           courses=courses)


