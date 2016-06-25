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
    PUB = _Department(u'pub', u'公共教学部', u'kouweili')

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
                   CntPermission.COLLEGE |
                   CntPermission.USER)


class _CntRoleSecretary(object):
    label = u'secretary'
    name = u'教学秘书'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
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
    PAPERS1 = _Material(u'papers1', u'06试卷Ａ')
    ANSWERS1 = _Material(u'answers1', u'07参考答案A')
    PAPERS2 = _Material(u'papers2', u'08试卷B')
    ANSWERS2 = _Material(u'answers2', u'09参考答案B')
    EXAMINATION1 = _Material(u'examination1', u'10考卷')
    SCORE1 = _Material(u'score1', u'11成绩表')
    EXAMINATION2 = _Material(u'examination2', u'12补考卷')
    SCORE2 = _Material(u'score2', u'13补考成绩表')
    SUMMARY = _Material(u'summary', u'教学小结')

    _objects = [SYLLABUS, EVALUATION, LECTURES, SCHEDULE, REPORT,
                PAPERS1, ANSWERS1, PAPERS2, ANSWERS2,
                EXAMINATION1, SCORE1, EXAMINATION2, SCORE2,
                SUMMARY]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getMaterialName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'00未知'


class CntPracticeMaterials(object):
    _Material = collections.namedtuple('_Material', ['label', 'name'])

    SYLLABUS = _Material(u'syllabus', u'01实习大纲')
    SCHEDULE = _Material(u'schedule', u'02实习计划')
    INSTRUCTION = _Material(u'instruction', u'03指导书')
    ROSTER = _Material(u'roster', u'04名单及分组表')
    REPORT = _Material(u'report', u'05学生实习报告')
    ACHIEVEMENT = _Material(u'achievement', u'06实习成果')
    SUMMARY = _Material(u'summary', u'07实习总结')

    _objects = [SYLLABUS, SCHEDULE, INSTRUCTION,
                ROSTER, REPORT,
                ACHIEVEMENT, SUMMARY]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getMaterialName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'00未知'



