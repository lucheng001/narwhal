# -*- coding: utf-8 -*-

import random
from application import create_app
from application.constants import CntRoles
from application.extensions import db


def generateCourses():
    app = create_app('default')
    from application.models import User, Course
    database = db.database

    database.connect()

    query = (User
             .select()
             .where(User.role == CntRoles.TEACHER.label))
    instructors = [row for row in query]

    courses = [u'大学语文', u'大学英语', u'大学物理', u'大学化学',
               u'高等数学', u'线性代数', u'思想品德修养', u'中国近代史',
               u'法律基础', u'编程导论', u'计算思维', u'数据库原理',
               u'计算机网络', u'操作系统原理', u'数据库原理']
    a = 2
    b = 5
    for instructor in instructors:
        numOfCourses = random.randint(a, b)
        for n in range(1, numOfCourses):
            Course.create(
                name=random.choice(courses),
                creator=instructor
            )

    database.close()

if __name__ == '__main__':
    generateCourses()
