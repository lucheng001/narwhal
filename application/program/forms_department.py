# -*- coding: utf-8 -*-

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..constants import CntAllowedExtensions

_all_ = ['UploadMaterialsForm']


class UploadMaterialsForm(Form):
    materials = FileField(
        u'文件',
        validators=[
            FileRequired(u'必须上传文件.'),
            FileAllowed(CntAllowedExtensions.choices, u'不允许上传此类文件.')
        ]
    )


