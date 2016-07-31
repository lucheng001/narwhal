# -*- coding: utf-8 -*-

import os
import math
import datetime
import uuid
import shutil
from urllib.parse import quote
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, request, abort, send_from_directory
from flask_login import login_required, current_user
from playhouse.flask_utils import get_object_or_404
from ..constants import CntPermission
from ..utilities import Paginator, permission_required
from ..models import User, Notice
from .forms_notice import AddNoticeForm
from . import bpNotice

_all_ = ['all', 'download']


@bpNotice.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def all():
    me = current_user
    if me.hasPermission(CntPermission.NOTICE):
        template = 'notice/college/all.html'
    else:
        template = 'notice/teacher/all.html'

    currentPage = request.args.get('currentPage', 1, type=int)

    numOfNotices = Notice.select().count()
    numOfPerPage = current_app.config['APP_ITEMS_PER_PAGE']
    numOfPages = int(math.ceil(float(numOfNotices) / float(numOfPerPage)))
    currentPage = currentPage if currentPage > 0 else 1
    currentPage = currentPage if currentPage <= numOfPages else numOfPages
    pagination = Paginator(object_num=numOfNotices, current=currentPage, per_page=numOfPerPage)

    if numOfNotices <= 0:
        return render_template(template, pagination=pagination,
                               notices=[])

    query = (Notice
             .select(Notice, User.chineseName)
             .join(User)
             .order_by(Notice.createTime.desc())
             .paginate(currentPage, numOfPerPage))
    notices = [row for row in query]
    return render_template(template, pagination=pagination,
                           notices=notices)


@bpNotice.route('/download/<int:noticeId>', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def download(noticeId):
    notice = get_object_or_404(Notice, (Notice.id == noticeId))
    name = notice.name
    uuidFileName, fExtension = notice.fileInfo.split('|')
    patternFileName = u'{uuid}.{ext}'
    fileName = patternFileName.format(uuid=uuidFileName, ext=fExtension)

    pattern = u'{name}.{ext}'
    normalFileName = pattern.format(name=name, ext=fExtension)
    encodeFileName = quote(normalFileName.encode('UTF-8'))

    filePath = current_app.config['APP_NOTICE_FOLDER']
    return send_from_directory(filePath, fileName,
                               as_attachment=True,
                               attachment_filename=encodeFileName)

