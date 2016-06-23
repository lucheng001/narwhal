# -*- coding: utf-8 -*-

import collections

_all_ = ['CntAllowedExtensions', 'CntGender', 'CntPermission', 'CntRoles', 'CntSyllabusYear']


class CntSyllabusYear(object):
    _SyllabusYear = collections.namedtuple('_SyllabusYear', ['label', 'name'])

    Y2012 = _SyllabusYear(u'2012版', u'2012')

    _objects = [Y2012]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels


class CntAllowedExtensions(object):
    _extensions = ['txt', 'doc', 'docx', 'pdf', 'rar', 'zip']
    _objects = list(set(_extensions + [ext.upper() for ext in _extensions]))

    choices = _objects
    labels = _objects


class CntGender(object):
    MALE = u'男'
    FEMALE = u'女'

    _objects = [MALE, FEMALE]

    choices = [(obj, obj) for obj in _objects]
    labels = _objects


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
    def getRolePermission(cls, role_label):
        role = cls._maps[role_label]
        return role.permissions if role_label in cls._labels else 0b0

    @classmethod
    def getRoleName(cls, role_label):
        role = cls._maps[role_label]
        return role.name if role_label in cls._labels else u'无角色'


