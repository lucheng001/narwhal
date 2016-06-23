# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, DateTimeField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length


class AddCourseForm(Form):
    name = StringField(
        u'名称',
        validators=[
            DataRequired(u'名称不能为空.'),
            Length(4, 32, u'名称为4~32个字符.'),
        ]
    )
    endTime = DateTimeField(
        u'截止日期',
        format='%Y-%m-%d',
        validators=[
            DataRequired(u'截止日期不能为空.')
        ]
    )
    minTime = DateTimeField(
        u'截止日期',
        format='%Y-%m-%d',
        validators=[
            DataRequired(u'结束日期超出范围.')
        ]
    )
    maxTime = DateTimeField(
        u'截止日期',
        format='%Y-%m-%d',
        validators=[
            DataRequired(u'结束日期超出范围.')
        ]
    )

    @staticmethod
    def validate_endTime(form, filed):
        minTime = form.minTime.data
        maxTime = form.maxTime.data
        endTime = filed.data

        if endTime < minTime or endTime > maxTime:
            raise ValidationError(u'结束日期超出范围.')


