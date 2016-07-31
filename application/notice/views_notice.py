# -*- coding: utf-8 -*-

import os
import datetime
import uuid
import shutil
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from playhouse.flask_utils import get_object_or_404
from ..constants import CntPermission
from ..utilities import permission_required
from ..models import Notice
from .forms_notice import AddNoticeForm
from . import bpNotice

_all_ = ['add', 'delete']


@bpNotice.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(CntPermission.NOTICE)
def add():
    me = current_user

    filePath = current_app.config['APP_NOTICE_FOLDER']

    form = AddNoticeForm()
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

        uuidFileName = str(uuid.uuid1())

        patternFileName = u'{uuid}.{ext}'
        fileName = patternFileName.format(uuid=uuidFileName, ext=fExtension)
        form.materials.data.save(os.path.join(filePath, fileName))

        patternFileInfo = u'{uuid}|{ext}'
        fileInfo = patternFileInfo.format(uuid=uuidFileName, ext=fExtension)
        Notice.create(
            creator=me.id,
            name=form.name.data,
            fileInfo=fileInfo
        )
        flash(u'通知发布成功', 'success')
        return redirect(url_for('.all'))

    return render_template('notice/college/add.html', form=form)


@bpNotice.route('/delete/<int:noticeId>', methods=['GET'])
@login_required
@permission_required(CntPermission.NOTICE)
def delete(noticeId):
    me = current_user
    notice = get_object_or_404(Notice, (Notice.id == noticeId))

    if notice.creator_id != me.id:
        abort(403)

    name = notice.name
    uuidFileName, fExtension = notice.fileInfo.split('|')
    patternFileName = u'{uuid}.{ext}'
    fileName = patternFileName.format(uuid=uuidFileName, ext=fExtension)

    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileName))
    filePath = os.path.join(current_app.config['APP_NOTICE_FOLDER'], fileName)

    shutil.move(filePath, recyclePath)

    notice.delete_instance()

    flash(u'通知删除成功', 'success')
    return redirect(url_for('.all'))


