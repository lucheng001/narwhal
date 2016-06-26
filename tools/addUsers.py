# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash
from application import create_app
from application.constants import CntRoles
from application.extensions import db

group1 = [
   ('diguangzhi', '狄光智'),
   ('zhangyan', '张雁'),
   ('zhangqinghui', '张晴晖'),
   ('wuxuelong', '伍学龙')
]

group2 = [
   ('yangweiwei', '杨微微')
]

group3 = [
   ('zhaojiagang', '赵家刚'),
   ('xuquanyuan', '徐全元'),
   ('lvdanjie', '吕丹桔'),
   ('kouweili', '寇卫利')
]

group4 = [
    ('caoyong', '曹涌'),
    ('chenxu', '陈旭'),
    ('chenyongren', '陈勇仁'),
    ('daizhengquan', '戴正权'),
    ('dongjiane', '董建娥'),
    ('dongyueyu', '董跃宇'),
    ('fuxiaoyong', '付小勇'),
    ('gaohao', '高皜'),
    ('guoran', '郭冉'),
    ('hanxu', '韩旭'),
    ('hejinping', '贺金平'),
    ('hexin', '何鑫'),
    ('hugangyi', '胡刚毅'),
    ('lijunqiu', '李俊萩'),
    ('linhong', '林宏'),
    ('lisha', '李莎'),
    ('luning', '鲁宁'),
    ('luying', '鲁莹'),
    ('miaocheng', '苗晟'),
    ('qiangzhenping', '强振平'),
    ('qinmingming', '秦明明'),
    ('rongjian', '荣剑'),
    ('sunyongke', '孙永科'),
    ('wanghuan', '王欢'),
    ('wangwei', '王维'),
    ('wangxiaolin', '王晓林'),
    ('wangxiaorui', '王晓锐'),
    ('xieshijian', '谢时俭'),
    ('xinghong', '幸宏'),
    ('xingliwei', '邢丽伟'),
    ('xiongfei', '熊飞'),
    ('xuweiheng', '徐伟恒'),
    ('yangpengyu', '杨鹏宇'),
    ('yangweimin', '杨为民'),
    ('yangyufeng', '杨雨峰'),
    ('yangyuyan', '杨雨燕'),
    ('yuyueyun', '禹玥昀'),
    ('zhanghongxiang', '张宏翔'),
    ('zhaofan', '赵璠'),
    ('zhaofangting', '赵芳婷'),
    ('zhaoyili', '赵毅力'),
    ('zhaoyoujie', '赵友杰'),
    ('zhonglihui', '钟丽辉'),
    ('zhoukailai', '周开来')
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
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.SECRETARY.label,
            permission=CntRoles.getRolePermission(CntRoles.SECRETARY.label)
        )

    for user in group3:
        User.create(
            userName=user[0],
            chineseName=user[1],
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.DIRECTOR.label,
            permission=CntRoles.getRolePermission(CntRoles.DIRECTOR.label)
        )

    for user in group4:
        User.create(
            userName=user[0],
            chineseName=user[1],
            password=password,
            passwordHash=generate_password_hash(password),
            role=CntRoles.TEACHER.label,
            permission=CntRoles.getRolePermission(CntRoles.TEACHER.label)
        )

    database.close()

if __name__ == '__main__':
    addUsers()



