# -*- coding: utf-8 -*-

import collections

_all_ = ['CntAllowedExtensions',
         'CntGender',
         'CntPermission',
         'CntRoles',
         'CntSyllabusYear',
         'CntDepartment'
         'CntCourseMaterials',
         'CntProgramMaterials',
         'CntThesisMaterials']


class CntAllowedExtensions(object):
    TEXT_TYPE = ['txt', 'pdf']
    MSOFFICE_TYPE = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
    IMAGE_TYPE = ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'svg']
    COMPRESS_TYPE = ['7z', 'rar', 'zip', 'bz2', 'gz', 'tar']

    _extensions = TEXT_TYPE + MSOFFICE_TYPE + IMAGE_TYPE + COMPRESS_TYPE
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
    Y2016 = _SyllabusYear(u'2016', u'2016版')

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
    EIE = _Department(u'eie', u'电子信息工程', u'lvdanjv')
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
    def getDepartmentDirectorName(cls, label):
        return cls._maps[label].director if label in cls._labels else u'未知'

    @classmethod
    def isDirector(cls, label, userName):
        return cls._maps[label].director == userName if label in cls._labels else False

    @classmethod
    def witchDepartment(cls, userName):
        label = u''
        for o in cls._objects:
            if userName == o.director:
                label = o.label
                break
        return label


class CntPermission(object):
    NOPERMISSION = 0b000000000000
    NORMAL       = 0b000000000001
    COURSE       = 0b000000000010
    PRACTICE     = 0b000000000100
    PROGRAM      = 0b000000001000
    DEPARTMENT   = 0b000000010000
    COLLEGE      = 0b000000100000
    USER         = 0b000001000000
    NOTICE       = 0b000010000000
    SUPPORT      = 0b000100000000
    THESIS       = 0b001000000000


class _CntRoleAdministrator(object):
    label = u'administrator'
    name = u'管理员'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.PRACTICE |
                   CntPermission.PROGRAM |
                   CntPermission.DEPARTMENT |
                   CntPermission.COLLEGE |
                   CntPermission.USER |
                   CntPermission.NOTICE |
                   CntPermission.SUPPORT |
                   CntPermission.THESIS)


class _CntRoleLeader(object):
    label = u'leader'
    name = u'学院领导'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.PRACTICE |
                   CntPermission.PROGRAM |
                   CntPermission.COLLEGE |
                   CntPermission.USER |
                   CntPermission.NOTICE |
                   CntPermission.SUPPORT |
                   CntPermission.THESIS)


class _CntRoleSecretary(object):
    label = u'secretary'
    name = u'教学秘书'
    permissions = (CntPermission.NORMAL |
                   CntPermission.COURSE |
                   CntPermission.PRACTICE |
                   CntPermission.PROGRAM |
                   CntPermission.COLLEGE |
                   CntPermission.USER|
                   CntPermission.NOTICE |
                   CntPermission.SUPPORT |
                   CntPermission.THESIS)


class _CntRoleDirector(object):
    label = u'director'
    name = u'教研室主任'
    permissions = (CntPermission.NORMAL |
                   CntPermission.PROGRAM |
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
    PAPERS1 = _Material(u'papers1', u'06试卷A')
    ANSWERS1 = _Material(u'answers1', u'07参考答案A')
    PAPERS2 = _Material(u'papers2', u'08试卷B')
    ANSWERS2 = _Material(u'answers2', u'09参考答案B')
    EXAMINATION1 = _Material(u'examination1', u'10学生考卷')
    SCORE1 = _Material(u'score1', u'11成绩表')
    EXAMINATION2 = _Material(u'examination2', u'12学生补考卷')
    SCORE2 = _Material(u'score2', u'13补考成绩表')
    ANALYSIS = _Material(u'analysis', u'14试卷分析报告')
    SUMMARY = _Material(u'summary', u'15教学小结')

    _objects = [SYLLABUS, EVALUATION, LECTURES, SCHEDULE, REPORT,
                PAPERS1, ANSWERS1, PAPERS2, ANSWERS2,
                EXAMINATION1, SCORE1, EXAMINATION2, SCORE2,
                ANALYSIS, SUMMARY]

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


class CntProgramMaterials(object):
    _Material = collections.namedtuple('_Material', ['label', 'name'])

    SYLLABUS = _Material(u'syllabus', u'01教学大纲')
    EVALUATION = _Material(u'evaluation', u'02考核大纲')
    PLAN = _Material(u'plan', u'03实习大纲')

    _objects = [SYLLABUS, EVALUATION, PLAN]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getMaterialName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'00未知'


class CntThesisMaterials(object):
    _Material = collections.namedtuple('_Material', ['label', 'name'])

    MANDATE = _Material(u'mandate', u'01任务书')
    SCHEDULE1 = _Material(u'schedule1', u'02指导计划表(教师)')
    SCHEDULE2 = _Material(u'schedule2', u'03指导计划表(学生)')
    PROPOSAL = _Material(u'proposal', u'04开题报告')
    CHECKLIST = _Material(u'checklist', u'05中期检查表')
    PPT1 = _Material(u'ppt1', u'06中期检答辩PPT')
    DEFENCE = _Material(u'defence', u'07答辩申请表')
    ADVICE = _Material(u'advice', u'08导教师意见')
    REVIEW = _Material(u'review', u'09评阅意见')
    THESIS = _Material(u'thesis', u'10论文')
    PPT2 = _Material(u'ppt2', u'11答辩PPT')
    SCORE = _Material(u'score', u'12成绩登记表')
    SOURCECODE = _Material(u'sourcecode', u'13源代码')

    _objects = [MANDATE, SCHEDULE1, SCHEDULE2, PROPOSAL, CHECKLIST,
                PPT1, DEFENCE, ADVICE, REVIEW,
                THESIS, PPT2, SCORE, SOURCECODE]

    _labels = [obj.label for obj in _objects]
    _maps = dict(zip(_labels, _objects))

    choices = [(obj.label, obj.name) for obj in _objects]
    labels = _labels

    @classmethod
    def getMaterialName(cls, label):
        return cls._maps[label].name if label in cls._labels else u'00未知'


