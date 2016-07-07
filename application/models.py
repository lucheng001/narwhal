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
    analysis = CharField(max_length=128, null=True)
    summary = CharField(max_length=128, null=True)
    syllabusYear = CharField(max_length=32, index=True, choices=CntSyllabusYear.choices, default=CntSyllabusYear.Y2012.label)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    _MATERIAL = CntCourseMaterials

    @classmethod
    def getTplMaterialName(cls, category):
        pattern = u'{name}.未交'
        material = pattern.format(name=cls._MATERIAL.getMaterialName(category))
        return material

    @classmethod
    def getMaterialNamePattern(cls, category):
        tpl = [cls._MATERIAL.getMaterialName(category),
               u'-{idx:02d}.{ext}']
        return u''.join(tpl)

    def getFolder(self, teacherName):
        pattern = u'{teacherName}-{name}-{klass}'
        folder = pattern.format(
            teacherName=teacherName,
            name=self.name,
            klass=self.klass)
        return folder

    def getFolderPath(self, teacherName):
        return os.path.join(self.semester, self.getDepartmentName(), self.getFolder(teacherName))

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    @classmethod
    def getMaterialName(cls, label):
        return cls._MATERIAL.getMaterialName(label)

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

    _MATERIAL = CntPracticeMaterials

    @classmethod
    def getTplMaterialName(cls, category):
        pattern = u'{name}.未交'
        material = pattern.format(name=cls._MATERIAL.getMaterialName(category))
        return material

    @classmethod
    def getMaterialNamePattern(cls, category):
        tpl = [cls._MATERIAL.getMaterialName(category),
               u'-{idx:02d}.{ext}']
        return u''.join(tpl)

    def getFolder(self, teacherName):
        pattern = u'{teacherName}-{name}-{klass}'
        folder = pattern.format(
            teacherName=teacherName,
            name=self.name,
            klass=self.klass)
        return folder

    def getFolderPath(self, teacherName):
        return os.path.join(self.semester, self.getDepartmentName(), self.getFolder(teacherName))

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    @classmethod
    def getMaterialName(cls, label):
        return cls._MATERIAL.getMaterialName(label)

    class Meta:
        database = db.database


class Program(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=256, index=True)
    department = CharField(max_length=32, index=True)
    theory = IntegerField(default=0)
    laboratory = IntegerField(default=0)
    practice = DecimalField(default=0.0, max_digits=4, decimal_places=2)
    syllabus = CharField(max_length=128, null=True)
    evaluation = CharField(max_length=128, null=True)
    plan = CharField(max_length=128, null=True)
    syllabusYear = CharField(max_length=32, index=True, choices=CntSyllabusYear.choices, default=CntSyllabusYear.Y2012.label)
    createTime = DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    _MATERIAL = CntProgramMaterials

    @classmethod
    def getTplMaterialName(cls, category):
        pattern = u'{name}.未交'
        material = pattern.format(name=cls._MATERIAL.getMaterialName(category))
        return material

    def getMaterialNamePattern(self, category):
        pattern = u'-{name}-{theory:03d}+{laboratory:03d}+{practice:.1f}'
        material = pattern.format(
            name=self.name,
            theory=self.theory,
            laboratory=self.laboratory,
            practice=self.practice)
        tpl = [self._MATERIAL.getMaterialName(category),
               material,
               u'-{idx:02d}.{ext}']
        return u''.join(tpl)

    def getFolder(self):
        pattern = u'{name}-{theory:03d}+{laboratory:03d}+{practice:.1f}'
        folder = pattern.format(
            name=self.name,
            theory=self.theory,
            laboratory=self.laboratory,
            practice=self.practice)
        return folder

    def getFolderPath(self):
        return os.path.join(self.syllabusYear, self.getDepartmentName(), self.getFolder())

    def getDepartmentName(self):
        return CntDepartment.getDepartmentName(self.department)

    def getSyllabusYearName(self):
        return CntSyllabusYear.getSyllabusYearName(self.syllabusYear)

    @classmethod
    def getMaterialName(cls, label):
        return cls._MATERIAL.getMaterialName(label)

    class Meta:
        database = db.database



