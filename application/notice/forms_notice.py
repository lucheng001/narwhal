# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..constants import CntAllowedExtensions


class AddNoticeForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 256, u'名称为4~256个字符.'),
        ]
    )
    materials = FileField(
        u'文件',
        validators=[
            FileRequired(u'必须上传文件.'),
            FileAllowed(CntAllowedExtensions.choices, u'不允许上传此类文件.')
        ]
    )
