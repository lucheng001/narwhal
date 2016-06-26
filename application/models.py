# -*- coding: utf-8 -*-

import os
import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from peewee import *
from .extensions import db
from .constants import (CntGender, CntRoles, CntSyllabusYear, CntDepartment,
                        CntCourseMaterials, CntPracticeMaterials, CntProgramMaterials)

_all_ = ['User', 'Course', 'Practice', 'Program']


class User(UserMixin, Model):
    id = PrimaryKeyField()
    userName = CharField(max_length=16, unique=True, index=True)
    chineseName = CharField(max_length=32, index=True)
    gender = CharField(max_length=8, index=True, choices=CntGender.choices, default=CntGender.MALE.label)
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

    def getGenderName(self):
        return CntGender.getGenderName(self.gender)

    class Meta:
        database = db.database


class Course(Model):
    id = PrimaryKeyField()
    teacher = ForeignKeyField(User)
    name = CharField(max_length=256, index=True)
    klass = CharField(max_length=256, index=True)
    semester = CharField(max_length=32, index=True)
    department = CharField(max_length=32, index=True)
    syllabus = CharField(max_length=128, null=True)
    evaluation = CharField(max_length=128, null=True)
    lectures = CharField(max_length=128, null=True)
    schedule = CharField(max_length=128, null=True)
    report = CharField(max_length=128, null=True)
    papers1 = CharField(max_length=128, null=True)
    answers1 = CharField(max_length=128, null=True)
    papers2 = CharField(max_length=128, null=True)
    answers2 = CharField(max_length=128, null=True)
    examination1 = CharField(max_length=128, null=True)
    score1 = CharField(max_length=128, null=True)
    examination2 = CharField(max_length=128, null=True)
    score2 = CharField(max_length=128, null=True)
    summary = CharField(max_length=128, null=True)
    syllabusYear = CharField(max_length=32, index=True, choices=CntSyllabusYear.choices, default=CntSyllabusYear.Y2012.label)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def getTplFileName(category):
        p = u'{name}.未交'
        tplFileName = p.format(name=CntCourseMaterials.getMaterialName(category)),
        return tplFileName

    def getFileNamePattern(self, category):
        tpl = [CntCourseMaterials.getMaterialName(category),
               u'-{idx:02d}.{ext}']
        return u''.join(tpl)

    def getFolder(self, teacher):
        return os.path.join(self.semester, self.getDepartmentName(),
                            teacher, self.name, self.klass)

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    def getMaterialName(self, label):
        return CntCourseMaterials.getMaterialName(label)

    class Meta:
        database = db.database


class Practice(Model):
    id = PrimaryKeyField()
    teacher = ForeignKeyField(User)
    name = CharField(max_length=256, index=True)
    klass = CharField(max_length=256, index=True)
    semester = CharField(max_length=32, index=True)
    department = CharField(max_length=32, index=True)
    syllabus = CharField(max_length=128, null=True)
    schedule = CharField(max_length=128, null=True)
    instruction = CharField(max_length=128, null=True)
    roster = CharField(max_length=128, null=True)
    report = CharField(max_length=128, null=True)
    summary = CharField(max_length=128, null=True)
    achievement = CharField(max_length=128, null=True)
    syllabusYear = CharField(max_length=32, index=True, choices=CntSyllabusYear.choices, default=CntSyllabusYear.Y2012.label)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def getTplFileName(category):
        p = u'{name}.未交'
        tplFileName = p.format(name=CntPracticeMaterials.getMaterialName(category)),
        return tplFileName

    def getFileNamePattern(self, category):
        tpl = [CntPracticeMaterials.getMaterialName(category),
               u'-{idx:02d}.{ext}']
        return u''.join(tpl)

    def getFolder(self, teacher):
        return os.path.join(self.semester, self.getDepartmentName(),
                            teacher, self.name, self.klass)

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    def getMaterialName(self, label):
        return CntPracticeMaterials.getMaterialName(label)

    class Meta:
        database = db.database


class Program(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=256, index=True)
    department = CharField(max_length=32, index=True)
    theory = IntegerField(default=0)
    laboratory = IntegerField(default=0)
    practice = IntegerField(default=0)
    syllabus = CharField(max_length=128, null=True)
    evaluation = CharField(max_length=128, null=True)
    syllabusYear = CharField(max_length=32, index=True, choices=CntSyllabusYear.choices, default=CntSyllabusYear.Y2012.label)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def getTplFileName(category):
        p = u'{name}.未交'
        tplFileName = p.format(name=CntProgramMaterials.getMaterialName(category)),
        return tplFileName

    def getFileNamePattern(self, category):
        p = u'-{name}-{theory:03d}_{laboratory:03d}_{practice:03d}'
        pattern = p.format(
            name=self.name,
            theory=self.theory,
            laboratory=self.laboratory,
            practice=self.practice),
        tpl = [CntProgramMaterials.getMaterialName(category),
               pattern,
               u'-{idx:02d}.{ext}']
        return u''.join(tpl)

    def getFolder(self):
        p = u'-{name}-{theory:03d}+{laboratory:03d}+{practice:03d}'
        pattern = p.format(
            name=self.name,
            theory=self.theory,
            laboratory=self.laboratory,
            practice=self.practice),
        return os.path.join(self.syllabusYear, self.getDepartmentName(), pattern)

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    def getMaterialName(self, label):
        return CntProgramMaterials.getMaterialName(label)

    class Meta:
        database = db.database



