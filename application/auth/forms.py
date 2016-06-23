# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, IPAddress


class LoginForm(Form):
    userName = StringField(
        u'用户名',
        validators=[
            DataRequired(u'用户名不能为空.'),
            Length(4, 16, u'用户名为4~16个字符.'),
        ]
    )
    password = PasswordField(
        u'密码',
        validators=[
            DataRequired(u'密码不能为空.'),
            Length(6, 16, u'密码为6~16个字符.')
        ]
    )
    remember = BooleanField(u'自动登录')

    clientIP = StringField(
        u'clientIP',
        validators=[
            DataRequired(u'IP不能为空'),
            IPAddress(u'不合法的IP地址.')
        ]
    )
    deviceName = StringField(u'deviceName')
    osName = StringField(u'osName')
    osVersion = StringField(u'osVersion')
    browserName = StringField(u'browserName')
    browserVersion = StringField(u'browserVersion')
    engineName = StringField(u'engineName')
    engineVersion = StringField(u'engineVersion')

