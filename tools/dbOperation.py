# -*- coding: utf-8 -*-

from application import create_app
from application.extensions import db


def reGenerateTables():
    app = create_app('default')
    from application.models import (Program)
    database = db.database
    database.connect()
    database.drop_tables([Program],
                         safe=True)
    database.create_tables([Program])
    database.close()

if __name__ == '__main__':
    reGenerateTables()

