# -*- coding: utf-8 -*-

import re
from flask_wtf import Form
from wtforms import StringField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..constants import CntAllowedExtensions


class AddDirectoryForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(2, 256, u'名称为2~256个字符.'),
        ]
    )

    @staticmethod
    def validate_name(form, filed):
        regx = re.compile(r'/+|\\+|\?+|%+|\*+|:+|\|+|\.+|\s+')
        if re.search(regx, filed.data):
            raise ValidationError(u'名称不合法.')


class AddFileForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(2, 256, u'名称为2~256个字符.'),
        ]
    )
    materials = FileField(
        u'文件',
        validators=[
            FileRequired(u'必须上传文件.'),
            FileAllowed(CntAllowedExtensions.choices, u'不允许上传此类文件.')
        ]
    )

    @staticmethod
    def validate_name(form, filed):
        regx = re.compile(r'/+|\\+|\?+|%+|\*+|:+|\|+|\.+|\s+')
        if re.search(regx, filed.data):
            raise ValidationError(u'名称不合法.')




