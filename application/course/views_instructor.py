# -*- coding: utf-8 -*-

import math
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from ..models import User, Course, CourseStudent, Task, Attendance
from ..constants import CntPermission
from ..utilities import Paginator, permission_required
from .forms_instructor import AddCourseForm
from . import bpCourse


@bpCourse.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.INSTRUCTOR)
def add():
    me = current_user
    form = AddCourseForm()
    if form.validate_on_submit():
        Course.create(
            name=form.name.data,
            endTime=form.endTime.data,
            creator=me._get_current_object()
        )
        flash(u'课程添加成功', 'success')
        return redirect(url_for('.taught'))

    return render_template('course/instructor/add.html', form=form)


@bpCourse.route('/delete/<int:courseId>', methods=['GET'])
@login_required
@permission_required(CntPermission.INSTRUCTOR)
def delete(courseId):
    course = get_object_or_404(Course, (Course.id == courseId))
    me = current_user
    if course.creator_id != me.id:
        abort(403)

    numOfStudents = (CourseStudent
                     .select()
                     .where(CourseStudent.course == course)
                     .count())
    if numOfStudents != 0:
        flash(u'已有学生加入该课程，无法删除', 'error')
        return redirect(url_for('.taught'))

    numOfTasks = (Task
                  .select()
                  .where(Task.course == course)
                  .count())
    if numOfTasks != 0:
        flash(u'该课程中有相关作业，无法删除', 'error')
        return redirect(url_for('.taught'))

    numOfAttendances = (Attendance
                        .select()
                        .where(Attendance.course == course)
                        .count())
    if numOfAttendances != 0:
        flash(u'该课程中有相关考勤，无法删除', 'error')
        return redirect(url_for('.taught'))

    course.delete_instance()
    flash(u'课程删除成功', 'success')

    return redirect(url_for('.taught'))


@bpCourse.route('/taught', methods=['GET'])
@login_required
@permission_required(CntPermission.INSTRUCTOR)
def taught():
    me = current_user

    currentPage = request.args.get('currentPage', 1, type=int)
    numOfCourses = (Course
                    .select()
                    .where(Course.creator == me.id)
                    .count())
    numOfPerPage = current_app.config['PT_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfCourses) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfCourses, current=currentPage, per_page=numOfPerPage)

    if numOfCourses <= 0:
        return render_template('course/instructor/taught.html', pagination=pagination,
                               courses=[])
    from peewee import fn, JOIN
    query = (Course
             .select(Course, fn.COUNT(CourseStudent.student).alias('num_of_students'))
             .join(CourseStudent, JOIN.LEFT_OUTER)
             .where(Course.creator == me.id)
             .group_by(Course.id)
             .order_by(Course.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    courses = [row for row in query]
    return render_template('course/instructor/taught.html', pagination=pagination,
                           courses=courses)


@bpCourse.route('/roster/<int:courseId>', methods=['GET'])
@login_required
@permission_required(CntPermission.INSTRUCTOR)
def roster(courseId):
    me = current_user
    course = get_object_or_404(Course, (Course.id == courseId))
    if course.creator_id != me.id:
        abort(403)

    currentPage = request.args.get('currentPage', 1, type=int)
    numOfStudents = (CourseStudent
                     .select()
                     .where(CourseStudent.course == course.id)
                     .count())
    numOfPerPage = current_app.config['PT_ITEMS_PER_PAGE_LG']
    numOfPages = int(math.ceil(float(numOfStudents) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfStudents, current=currentPage, per_page=numOfPerPage)

    if numOfStudents <= 0:
        return render_template('course/instructor/roster.html', pagination=pagination,
                               course=course, students=[])

    query = (User
             .select(
			     User.id, 
			     User.userName, 
				 User.chineseName)
             .join(CourseStudent)
             .where(CourseStudent.course == course.id)
             .order_by(User.userName.asc())
             .paginate(currentPage, numOfPerPage))

    students = [row for row in query]
    return render_template('course/instructor/roster.html', pagination=pagination,
                           course=course, students=students)



