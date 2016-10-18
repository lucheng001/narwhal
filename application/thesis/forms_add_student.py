# -*- coding: utf-8 -*-

import re
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length
from ..constants import CntDepartment

_all_ = ['AddStudentForm', 'AddStudentDataForm']


class AddStudentForm(Form):
    studentNum = StringField(
        u'学号',
        validators=[
            DataRequired(u'学号不能为空.'),
            Length(11, 11, u'学号为11个字符.')
        ]
    )
    studentName = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(2, 10, u'名称为2~10个字符.')
        ]
    )
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 256, u'名称为4~256个字符.'),
        ]
    )
    teacher = SelectField(
        u'指导老师',
        coerce=int,
        validators=[DataRequired(u'指导老师不能为空')]
    )
    semester = StringField(
        u'学期',
        validators=[
            DataRequired(u'学期不能为空.'),
            Length(4, 4, u'学期为4个字符.'),
        ]
    )
    department = SelectField(
        u'教研室',
        validators=[DataRequired(u'教研室不能为空.')],
        choices=CntDepartment.choices
    )

    @staticmethod
    def validate_semester(form, filed):
        pattern = r'20\d{2}'
        match = re.match(pattern, filed.data)
        if not match:
            raise ValidationError(u'学期格式错误.')


class AddStudentDataForm(Form):
    studentData = TextAreaField(
        u'学生数据',
        validators=[
            DataRequired(u'学生数据不能为空.')
        ]
    )


