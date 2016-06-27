# -*- coding: utf-8 -*-

import hashlib
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, RadioField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from ..constants import CntGender
from ..models import User

_all_ = ['RegisterForm', 'ChangeChineseNameForm', 'ChangePasswordForm', 'ChangeProfile']


class ChangeChineseNameForm(Form):
    chineseName = StringField(
        u'姓名', validators=[
            DataRequired(u'姓名不能为空.'),
            Length(1, 32)
        ]
    )


class ChangePasswordForm(Form):
    oldPassword = PasswordField(
        u'旧密码',
        validators=[
            DataRequired(u'旧密码不能为空.'),
            Length(6, 16, u'密码为6~16个字符.')
        ]
    )
    newPassword = PasswordField(
        u'密码', validators=[
            DataRequired(u'密码不能为空.'),
            Length(6, 16, u'密码为6~16个字符.')
        ]
    )
    confirmPassword = PasswordField(
        u'确认密码',
        validators=[
            DataRequired(u'确认密码不能为空.'),
            Length(6, 16, u'确认密码为6~16个字符.'),
            EqualTo('newPassword', message=u'密码不匹配.')
        ]
    )


class RegisterForm(Form):
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
    vc = HiddenField(
        u'vc',
        validators=[
            DataRequired(u'验证码错误.'),
            Length(40, 40, u'验证码错误.')
        ]
    )
    ic = HiddenField(
        u'ic',
        validators=[
            DataRequired(u'邀请码错误.'),
            Length(40, 40, u'邀请码错误.')
        ]
    )
    verificationCode = StringField(
        u'验证码',
        validators=[
            DataRequired(u'验证码不能为空.'),
            Length(4, 4)
        ]
    )
    invitationCode = StringField(
        u'邀请码',
        validators=[
            DataRequired(u'邀请码不能为空.'),
            Length(4, 4)
        ]
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

    @staticmethod
    def validate_verificationCode(form, filed):
        vc = form.vc.data
        verificationCode = hashlib.sha1(filed.data.encode('utf-8')).hexdigest()

        if verificationCode != vc:
            raise ValidationError(u'验证码错误.')

    @staticmethod
    def validate_invitationCode(form, filed):
        ic = form.ic.data
        invitationCode = hashlib.sha1(filed.data.encode('utf-8')).hexdigest()

        if invitationCode != ic:
            raise ValidationError(u'邀请码错误.')


class ChangeProfileForm(Form):
    chineseName = StringField(
        u'姓名', validators=[
            DataRequired(u'姓名不能为空.'),
            Length(1, 32)
        ]
    )
    gender = RadioField(
        u'性别',
        validators=[DataRequired(u'性别不能为空')],
        choices=CntGender.choices
    )

