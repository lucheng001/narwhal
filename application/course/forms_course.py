# -*- coding: utf-8 -*-

import re
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length
from ..constants import CntDepartment

_all_ = ['AddCourseForm', 'AddCourseDataForm']


class AddCourseForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 32, u'名称为4~32个字符.'),
        ]
    )
    teacher = SelectField(
        u'名称',
        coerce=int,
        validators=[DataRequired(u'必须制定上课教师.')]
    )
    klass = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 265, u'名称为4~256个字符.'),
        ]
    )
    semester = StringField(
        u'学期',
        validators=[
            DataRequired(u'学期不能为空.'),
            Length(11, 11, u'学期为11个字符.'),
        ]
    )
    department = SelectField(
        u'教研室',
        validators=[DataRequired(u'教研室不能为空.')],
        choices=CntDepartment.choices
    )
    syllabusYear = StringField(
        u'培养方案',
        validators=[
            DataRequired(u'培养方案不能为空.'),
            Length(4, 4, u'培养方案为4个字符.'),
        ]
    )

    @staticmethod
    def validate_semester(form, filed):
        pattern = r'20\d{2}-20\d{2}-[1,2]'
        match = re.match(pattern, filed.data)
        if not match:
            raise ValidationError(u'学期格式错误.')

    @staticmethod
    def validate_syllabusYear(form, filed):
        pattern = r'20\d{2}'
        match = re.match(pattern, filed.data)
        if not match:
            raise ValidationError(u'培养方案格式错误.')


class AddCourseDataForm(Form):
    courseData = TextAreaField(
        u'课程数据',
        validators=[
            DataRequired(u'课程数据不能为空.')
        ]
    )


