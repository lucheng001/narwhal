# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange
from ..constants import CntDepartment, CntSyllabusYear

_all_ = ['AddProgramForm', 'AddProgramDataForm']


class AddProgramForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 265, u'名称为4~256个字符.'),
        ]
    )
    department = SelectField(
        u'教研室',
        validators=[DataRequired(u'教研室不能为空.')],
        choices=CntDepartment.choices
    )
    theory = IntegerField(
        u'理论学时',
        validators=[
            InputRequired(u'理论学时不能为空.'),
            NumberRange(min=0, message=u'不能小于零.')
        ]
    )
    laboratory = IntegerField(
        u'实验学时',
        validators=[
            InputRequired(u'实验学时不能为空.'),
            NumberRange(min=0, message=u'不能小于零.')
        ]
    )
    practice = IntegerField(
        u'实习周数',
        validators=[
            InputRequired(u'实习周数不能为空.'),
            NumberRange(min=0, message=u'不能小于零.')
        ]
    )
    syllabusYear = SelectField(
        u'培养方案年份',
        validators=[
            DataRequired(u'培养方案年份不能为空.')
        ],
        choices=CntSyllabusYear.choices
    )


class AddProgramDataForm(Form):
    programData = TextAreaField(
        u'培养方案数据',
        validators=[
            DataRequired(u'培养方案数据不能为空.')
        ]
    )



