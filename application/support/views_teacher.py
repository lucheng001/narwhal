# -*- coding: utf-8 -*-

import os
from urllib.parse import quote
from flask import render_template, redirect, url_for, flash, current_app, request, abort, send_from_directory
from flask_login import login_required, current_user
from playhouse.flask_utils import get_object_or_404
from ..constants import CntPermission
from ..utilities import Paginator, permission_required
from ..models import User, Support
from . import bpSupport

_all_ = ['all', 'download']


@bpSupport.route('/all/<int:parentId>', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def all(parentId):
    parent = get_object_or_404(Support, (Support.id == parentId))

    me = current_user
    if me.hasPermission(CntPermission.SUPPORT):
        template = 'support/college/all.html'
    else:
        template = 'support/teacher/all.html'

    query = (Support
             .select(Support, User.chineseName)
             .join(User)
             .where(Support.parent == parent.id)
             .order_by(Support.name.asc()))
    supports = [row for row in query]
    return render_template(template, parent=parent, supports=supports)


@bpSupport.route('/download/file/<int:supportId>', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def downloadFile(supportId):
    support = get_object_or_404(Support, (Support.id == supportId))
    fileName = support.name
    encodeFileName = quote(fileName.encode('UTF-8'))
    parent = support.parent
    filePath = os.path.join(current_app.config['APP_SUPPORT_FOLDER'], parent.getRelativePath())
    return send_from_directory(filePath, fileName,
                               as_attachment=True,
                               attachment_filename=encodeFileName)


