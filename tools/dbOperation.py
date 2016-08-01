# -*- coding: utf-8 -*-

from application import create_app
from application.extensions import db


def reGenerateTables():
    app = create_app('default')
    from application.models import (Support)
    database = db.database
    database.connect()
    database.drop_tables([Support],
                         safe=True)
    database.create_tables([Support])
    database.close()

if __name__ == '__main__':
    reGenerateTables()

