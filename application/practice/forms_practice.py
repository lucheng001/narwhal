# -*- coding: utf-8 -*-

import re
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length
from ..constants import CntDepartment, CntSyllabusYear

_all_ = ['AddPracticeForm', 'AddPracticeDataForm']


class AddPracticeForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 256, u'名称为4~256个字符.'),
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
            DataRequired(u'培养方案不能为空.')
        ],
        choices=CntSyllabusYear.choices
    )

    @staticmethod
    def validate_semester(form, filed):
        pattern = r'20\d{2}-20\d{2}-[1,2]'
        match = re.match(pattern, filed.data)
        if not match:
            raise ValidationError(u'学期格式错误.')
        y1, y2, _ = filed.data.split('-')
        y1 = int(y1)
        y2 = int(y2)
        if y2 != y1 + 1:
            raise ValidationError(u'学期格式错误.')


class AddPracticeDataForm(Form):
    practiceData = TextAreaField(
        u'实训数据',
        validators=[
            DataRequired(u'实训数据不能为空.')
        ]
    )


