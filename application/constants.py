# -*- coding: utf-8 -*-

import collections

_all_ = ['CntAllowedExtensions',
         'CntGender',
         'CntPermission',
         'CntRoles',
         'CntSyllabusYear',
         'CntDepartment'
         'CntCourseMaterials']


class CntAllowedExtensions(object):
    _extensions = ['txt', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'rar', 'zip']
    _objects = list(set(_extensions + [ext.upper() for ext in _extensions]))

    choices = _objects
    labels = _objects


class CntGender(object):
    _Gender = collections.namedtuple('_Gender', ['label', 'name'])

    MALE = _Gender(u'male', u'男')
    FEMALE = _Gender(u'female', u'女')

    _objects = [MALE, FEMALE]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getGenderName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'未知'


class CntSyllabusYear(object):
    _SyllabusYear = collections.namedtuple('_SyllabusYear', ['label', 'name'])

    Y2012 = _SyllabusYear(u'2012', u'2012版')

    _objects = [Y2012]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getSyllabusYearName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'未知'


class CntDepartment(object):
    _Department = collections.namedtuple('_Department', ['label', 'name', 'director'])

    CS = _Department(u'cs', u'计算机科学与技术', u'zhaojiagang')
    EST = _Department(u'est', u'电子科学与技术', u'xuquanyuan')
    EIE = _Department(u'eie', u'电子信息工程', u'lvdanju')
    IE = _Department(u'ie', u'信息工程', u'hukunrong')
    PUB = _Department(u'pub', u'公共', u'kouweili')

    _objects = [CS, EST, EIE, IE, PUB]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getDepartmentName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'未知'

    @classmethod
    def isDirector(cls, label, userName):
        return cls._maps[label].director == userName if label in cls._labels else False


class CntPermission(object):
    NOPERMISSION = 0b00000000
    NORMAL = 0b00000001
    COURSE = 0b00000010
    DEPARTMENT = 0b00000100
    COLLEGE = 0b00001000
    USER = 0b00010000


class _CntRoleAdministrator(object):
    label = u'administrator'
    name = u'管理员'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.DEPARTMENT |
                   CntPermission.COLLEGE |
                   CntPermission.USER)


class _CntRoleLeader(object):
    label = u'leader'
    name = u'院领导'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.DEPARTMENT |
                   CntPermission.COLLEGE |
                   CntPermission.USER)


class _CntRoleSecretary(object):
    label = u'secretary'
    name = u'教学秘书'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.DEPARTMENT |
                   CntPermission.COLLEGE |
                   CntPermission.USER)


class _CntRoleDirector(object):
    label = u'director'
    name = u'教研室主任'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.DEPARTMENT)


class _CntRoleTeacher(object):
    label = u'teacher'
    name = u'教师'
    permissions = CntPermission.NORMAL


class CntRoles(object):
    LEADER = _CntRoleLeader
    SECRETARY = _CntRoleSecretary
    DIRECTOR = _CntRoleDirector
    TEACHER = _CntRoleTeacher

    _objects = [LEADER, SECRETARY, DIRECTOR, TEACHER]
    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getRolePermission(cls, label):
        return cls._maps[label].permissions if label in cls._labels else 0b0

    @classmethod
    def getRoleName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'未知'


class CntCourseMaterials(object):
    _Material = collections.namedtuple('_Material', ['label', 'name'])

    SYLLABUS = _Material(u'syllabus', u'01教学大纲')
    EVALUATION = _Material(u'evaluation', u'02考核大纲')
    LECTURES = _Material(u'lectures', u'03教案')
    SCHEDULE = _Material(u'schedule', u'04教学进程表')
    REPORT = _Material(u'report', u'05学生实验报告')
    PAPERSA = _Material(u'papersA', u'06试卷Ａ')
    ANSWERSA = _Material(u'answersA', u'07参考答案A')
    PAPERSB = _Material(u'papersB', u'08试卷B')
    ANSWERSB = _Material(u'answersB', u'09参考答案B')
    SUMMARY = _Material(u'summary', u'09参考答案B')

    _objects = [SYLLABUS, EVALUATION, LECTURES, SCHEDULE, REPORT,
                PAPERSA, ANSWERSA, PAPERSB, ANSWERSB]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getMaterialName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'0未知'



