# -*- coding: utf-8 -*-

import os
import datetime
import shutil
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from playhouse.flask_utils import get_object_or_404
from ..constants import CntPermission
from ..utilities import permission_required
from ..models import Support
from .forms_support import AddDirectoryForm, AddFileForm
from . import bpSupport

_all_ = ['addDirectory', 'deleteDirectory', 'addFile', 'deleteFile']


@bpSupport.route('/add/directory/<int:parentId>', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.SUPPORT)
def addDirectory(parentId):
    me = current_user
    parent = get_object_or_404(Support, (Support.id == parentId))

    form = AddDirectoryForm()
    if form.validate_on_submit():
        parentPath = parent.getRelativePath()

        fullPath = os.path.join(current_app.config['APP_SUPPORT_FOLDER'],
                                parentPath, form.name.data)

        if os.path.isdir(fullPath):
            flash(u'文件夹已经存在', 'warning')
            return redirect(url_for('.all', parentId=parent.id))

        os.mkdir(fullPath)

        Support.create(
            parent=parent.id,
            name=form.name.data.strip(),
            creator=me.id
        )

        flash(u'文件夹创建成功', 'success')
        return redirect(url_for('.all', parentId=parent.id))

    return render_template('support/college/addDirectory.html', form=form,
                           parent=parent)


@bpSupport.route('/delete/directory/<int:supportId>', methods=['GET'])
@login_required
@permission_required(CntPermission.SUPPORT)
def deleteDirectory(supportId):
    me = current_user
    support = get_object_or_404(Support, (Support.id == supportId))

    if support.creator_id != me.id:
        abort(403)

    if not support.isDirectory:
        abort(404)

    if support.id == 1:
        flash(u'不能删除该文件夹', 'warning')
        return redirect(url_for('.all', parentId=1))

    parent = support.parent

    numOfChlidren = Support.select().where(Support.parent == support.id).count()
    if numOfChlidren > 0:
        flash(u'文件夹不为空', 'warning')
        return redirect(url_for('.all', parentId=parent.id))

    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    fileString = support.name
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileString))

    parentPath = parent.getRelativePath()
    filePath = os.path.join(current_app.config['APP_SUPPORT_FOLDER'],
                            parentPath, fileString)
    shutil.move(filePath, recyclePath)
    support.delete_instance()

    flash(u'文件夹删除成功', 'success')
    return redirect(url_for('.all', parentId=parent.id))


@bpSupport.route('/add/file/<int:parentId>', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.SUPPORT)
def addFile(parentId):
    me = current_user
    parent = get_object_or_404(Support, (Support.id == parentId))

    form = AddFileForm()
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

        parentPath = parent.getRelativePath()

        fullPath = os.path.join(current_app.config['APP_SUPPORT_FOLDER'],
                                parentPath)

        patternFileName = u'{name}.{ext}'
        fileName = patternFileName.format(name=form.name.data.strip(), ext=fExtension)
        if os.path.isfile(os.path.join(fullPath, fileName)):
            flash(u'文件已经存在', 'warning')
            return redirect(url_for('.all', parentId=parent.id))

        form.materials.data.save(os.path.join(fullPath, fileName))

        Support.create(
            parent=parent.id,
            name=fileName,
            isDirectory=False,
            creator=me.id
        )

        flash(u'文件上传成功', 'success')
        return redirect(url_for('.all', parentId=parent.id))

    return render_template('support/college/addFile.html', form=form,
                           parent=parent)


@bpSupport.route('/delete/file/<int:supportId>', methods=['GET'])
@login_required
@permission_required(CntPermission.SUPPORT)
def deleteFile(supportId):
    me = current_user
    support = get_object_or_404(Support, (Support.id == supportId))

    if support.creator_id != me.id:
        abort(403)

    if support.isDirectory:
        abort(404)

    parent = support.parent

    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    fileString = support.name
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileString))

    parentPath = parent.getRelativePath()
    filePath = os.path.join(current_app.config['APP_SUPPORT_FOLDER'],
                            parentPath, fileString)
    shutil.move(filePath, recyclePath)
    support.delete_instance()

    flash(u'文件删除成功', 'success')
    return redirect(url_for('.all', parentId=parent.id))

