# -*- coding: utf-8 -*-

import os
import shutil
from flask_login import login_required
from flask import flash, redirect, url_for, current_app
from playhouse.flask_utils import get_object_or_404
from datetime import  datetime
from ..models import Thesis
from ..utilities import permission_required
from ..constants import CntPermission
from . import bpThesis

@bpThesis.route('/delect/<int:thesisId>', methods=['GET'])
@login_required
@permission_required(CntPermission.THESIS)
def delect(thesisId):
    thesis = get_object_or_404(Thesis, (Thesis.id == thesisId))
    teacher = thesis.teacher

    timeString = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    fileString = thesis.getFolder(thesis.studentName)
    recyclePath = os.path.join(current_app.config['APP_RECYCLE_FOLDER'],
                               u'{}_{}'.format(timeString, fileString))
    filePath = os.path.join(current_app.config['APP_THESIS_FOLDER'],
                            thesis.getFolderPath(teacher.chineseName))

    # if os.path.isdir(filePath):
    #     shutil.rmtree(filePath)

    shutil.move(filePath, recyclePath)

    thesis.delete_instance()

    flash(u'删除成功', 'success')
    return redirect(url_for('bpThesis.all'))