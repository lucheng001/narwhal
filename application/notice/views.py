# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask_login import login_required
from ..constants import CntPermission
from ..utilities import permission_required
from . import bpNotice

_all_ = ['all']


@bpNotice.route('/all', methods=['GET'])
@login_required
@permission_required(CntPermission.NORMAL)
def all():
    return render_template('notice/all.html')




