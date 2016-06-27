# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, RadioField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from ..constants import CntRoles, CntGender
from ..models import User

_all_ = ['AddUserForm']


class AddUserForm(Form):
    userName = StringField(
        u'用户名',
        validators=[
            DataRequired(u'用户名不能为空.'),
            Length(4, 16, u'用户名为4~16个字符.'),
        ]
    )
    chineseName = StringField(
        u'姓名',
        validators=[
            DataRequired(u'姓名不能为空.'),
            Length(1, 32)
        ]
    )
    password = PasswordField(
        u'密码',
        validators=[
            DataRequired(u'密码不能为空.'),
            Length(6, 16, u'密码为6~16个字符.')
        ]
    )
    confirmPassword = PasswordField(
        u'确认密码',
        validators=[
            DataRequired(u'确认密码不能为空.'),
            Length(6, 16, u'确认密码为6~16个字符.'),
            EqualTo('password', message=u'密码不匹配.')
        ]
    )
    role = SelectField(
        u'角色',
        validators=[DataRequired(u'必须制定一个角色.')],
        choices=CntRoles.choices
    )
    gender = RadioField(
        u'性别',
        validators=[DataRequired(u'性别不能为空')],
        choices=CntGender.choices
    )

    @staticmethod
    def validate_userName(form, filed):
        user = None
        try:
            user = User.get(User.userName == filed.data)
        except User.DoesNotExist:
            user = None

        if user:
            raise ValidationError(u'用户名已经被使用.')




