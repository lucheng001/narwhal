# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash
from application import create_app
from application.constants import CntRoles
from application.extensions import db


def generateUsers():
    app = create_app('default')
    from application.models import User
    database = db.database
    instructors = [
        {'userName': 'zhaolaoshi', 'chineseName': u'赵老师', 'password': '123456'},
        {'userName': 'qianlaoshi', 'chineseName': u'钱老师', 'password': '123456'},
        {'userName': 'sunlaoshi', 'chineseName': u'孙老师', 'password': '123456'}
    ]

    database.connect()

    for instructor in instructors:
        User.create(
            userName=instructor['userName'],
            chineseName=instructor['chineseName'],
            password=instructor['password'],
            passwordHash=generate_password_hash(instructor['password']),
            role=CntRoles.INSTRUCTOR.label
        )

    database.close()

if __name__ == '__main__':
    generateUsers()



