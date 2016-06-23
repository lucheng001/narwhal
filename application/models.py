# -*- coding: utf-8 -*-

import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from peewee import *
from .extensions import db
from .constants import CntRoles, CntSyllabusYear, CntDepartment

_all_ = ['User', 'Course', 'Practice']


class User(UserMixin, Model):
    id = PrimaryKeyField()
    userName = CharField(max_length=16, unique=True, index=True)
    chineseName = CharField(max_length=32, index=True)
    role = CharField(max_length=32, index=True, choices=CntRoles.choices, default=CntRoles.TEACHER.label)
    permission = IntegerField(default=0)
    password = CharField(max_length=32)
    passwordHash = CharField(max_length=265)
    lastLoginTime = DateTimeField(default=datetime.datetime.min, formats='%Y-%m-%d %H:%M:%S')
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def verifyPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    def hasPermission(self, permissions):
        return (CntRoles.getRolePermission(self.role) & permissions) == permissions

    def getRoleName(self):
        return CntRoles.getRoleName(self.role)

    class Meta:
        database = db.database


class Course(Model):
    id = PrimaryKeyField()
    teacher = ForeignKeyField(User)
    name = CharField(max_length=32, index=True)
    klass = CharField(max_length=256, index=True)
    semester = CharField(max_length=32, index=True)
    department = CharField(max_length=32, index=True)
    syllabus = CharField(max_length=128, null=True)
    plans = CharField(max_length=128, null=True)
    schedule = CharField(max_length=128, null=True)
    report = CharField(max_length=128, null=True)
    evaluation = CharField(max_length=128, null=True)
    examinationA = CharField(max_length=128, null=True)
    answerA = CharField(max_length=128, null=True)
    examinationB = CharField(max_length=128, null=True)
    answerB = CharField(max_length=128, null=True)
    syllabusYear = CharField(max_length=32, index=True, choices=CntSyllabusYear, default=CntSyllabusYear.Y2012.label)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    class Meta:
        database = db.database


class Practice(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=32, index=True)
    teacher = ForeignKeyField(User)
    klass = CharField(max_length=256, index=True)
    semester = CharField(max_length=32, index=True)
    syllabus = CharField(max_length=128, null=True)
    plans = CharField(max_length=128, null=True)
    instruction = CharField(max_length=128, null=True)
    roster = CharField(max_length=128, null=True)
    report = CharField(max_length=128, null=True)
    summary = CharField(max_length=128, null=True)
    achievement = CharField(max_length=128, null=True)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = db.database





