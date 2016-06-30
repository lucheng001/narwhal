# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash
from application import create_app
from application.constants import CntRoles, CntGender
from application.extensions import db

group1 = [
   ('diguangzhi',   '狄光智',   CntGender.FEMALE.label),
   ('zhangyan',     '张雁',     CntGender.FEMALE.label),
   ('zhangqinghui', '张晴晖',   CntGender.MALE.label),
   ('wuxuelong',    '伍学龙',   CntGender.MALE.label)
]

group2 = [
   ('yangweiwei',   '杨微微',   CntGender.FEMALE.label)
]

group3 = [
   ('zhaojiagang',  '赵家刚',   CntGender.MALE.label),
   ('xuquanyuan',   '徐全元',   CntGender.MALE.label),
   ('lvdanjie',     '吕丹桔',   CntGender.FEMALE.label),
   ('kouweili',     '寇卫利',   CntGender.MALE.label)
]

group4 = [
    ('caoyong',           '曹涌',     CntGender.MALE.label),
    ('chenxu',            '陈旭',     CntGender.MALE.label),
    ('chenyongren',       '陈勇仁',    CntGender.MALE.label),
    ('daizhengquan',      '戴正权',    CntGender.MALE.label),
    ('dongjiane',         '董建娥',    CntGender.FEMALE.label),
    ('dongyueyu',         '董跃宇',    CntGender.MALE.label),
    ('fuxiaoyong',        '付小勇',    CntGender.MALE.label),
    ('gaohao',            '高皜',     CntGender.FEMALE.label),
    ('guoran',            '郭冉',     CntGender.MALE.label),
    ('hanxu',             '韩旭',     CntGender.MALE.label),
    ('hejinping',         '贺金平',   CntGender.MALE.label),
    ('hexin',             '何鑫',     CntGender.MALE.label),
    ('hugangyi',          '胡刚毅',    CntGender.MALE.label),
    ('lijunqiu',          '李俊萩',    CntGender.FEMALE.label),
    ('linhong',           '林宏',      CntGender.FEMALE.label),
    ('lisha',             '李莎',      CntGender.FEMALE.label),
    ('luning',            '鲁宁',      CntGender.MALE.label),
    ('luying',            '鲁莹',      CntGender.FEMALE.label),
    ('miaocheng',         '苗晟',      CntGender.MALE.label),
    ('qiangzhenping',     '强振平',    CntGender.MALE.label),
    ('qinmingming',       '秦明明',    CntGender.MALE.label),
    ('rongjian',          '荣剑',     CntGender.MALE.label),
    ('sunyongke',         '孙永科',   CntGender.MALE.label),
    ('wanghuan',          '王欢',     CntGender.MALE.label),
    ('wangwei',           '王维',     CntGender.FEMALE.label),
    ('wangxiaolin',       '王晓林',   CntGender.MALE.label),
    ('wangxiaorui',       '王晓锐',   CntGender.MALE.label),
    ('xieshijian',        '谢时俭',   CntGender.MALE.label),
    ('xinghong',          '幸宏',     CntGender.MALE.label),
    ('xingliwei',         '邢丽伟',   CntGender.FEMALE.label),
    ('xiongfei',          '熊飞',     CntGender.MALE.label),
    ('xuweiheng',         '徐伟恒',   CntGender.MALE.label),
    ('yangpengyu',        '杨鹏宇',   CntGender.MALE.label),
    ('yangweimin',        '杨为民',   CntGender.MALE.label),
    ('yangyufeng',        '杨雨峰',   CntGender.FEMALE.label),
    ('yangyuyan',         '杨雨燕',   CntGender.FEMALE.label),
    ('yuyueyun',          '禹玥昀',   CntGender.FEMALE.label),
    ('zhanghongxiang',    '张宏翔',   CntGender.MALE.label),
    ('zhaofan',           '赵璠',     CntGender.MALE.label),
    ('zhaofangting',      '赵芳婷',   CntGender.FEMALE.label),
    ('zhaoyili',          '赵毅力',   CntGender.MALE.label),
    ('zhaoyoujie',        '赵友杰',   CntGender.MALE.label),
    ('zhonglihui',        '钟丽辉',   CntGender.FEMALE.label),
    ('zhoukailai',        '周开来',   CntGender.MALE.label)
]


def addUsers():
    app = create_app('default')
    from application.models import User
    database = db.database

    password = app.config['APP_DEFAULT_PASSWORD']

    database.connect()

    for user in group1:
        User.create(
            userName=user[0],
            chineseName=user[1],
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.LEADER.label,
            permission=CntRoles.getRolePermission(CntRoles.LEADER.label)
        )

    for user in group2:
        User.create(
            userName=user[0],
            chineseName=user[1],
            gender=user[2],
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.SECRETARY.label,
            permission=CntRoles.getRolePermission(CntRoles.SECRETARY.label)
        )

    for user in group3:
        User.create(
            userName=user[0],
            chineseName=user[1],
            gender=user[2],
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.DIRECTOR.label,
            permission=CntRoles.getRolePermission(CntRoles.DIRECTOR.label)
        )

    for user in group4:
        User.create(
            userName=user[0],
            chineseName=user[1],
            gender=user[2],
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.TEACHER.label,
            permission=CntRoles.getRolePermission(CntRoles.TEACHER.label)
        )

    database.close()

if __name__ == '__main__':
    addUsers()



