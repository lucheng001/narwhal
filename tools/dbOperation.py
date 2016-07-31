# -*- coding: utf-8 -*-

from application import create_app
from application.extensions import db


def reGenerateTables():
    app = create_app('default')
    from application.models import (Notice)
    database = db.database
    database.connect()
    database.drop_tables([Notice],
                         safe=True)
    database.create_tables([Notice])
    database.close()

if __name__ == '__main__':
    reGenerateTables()

