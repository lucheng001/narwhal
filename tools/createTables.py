# -*- coding: utf-8 -*-

from application import create_app
from application.extensions import db


def createTables():
    app = create_app('default')
    from application.models import (User, Course, Practice, Program, Thesis)
    database = db.database
    database.connect()
    database.create_tables([User, Course, Practice, Program, Thesis])
    database.close()

if __name__ == '__main__':
    createTables()
