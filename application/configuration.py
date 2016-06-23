# -*- coding: utf-8 -*-

import os


class Configuration(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    BASE_DIR = os.path.abspath(os.path.dirname(APP_DIR))
    DATABASE = 'postgresql://narwhal:1234qwer@127.0.0.1:5432/narwhal'
    SECRET_KEY = 'ZVRymCEV7NRSpujp'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    APP_LOG_DIR = os.path.join(BASE_DIR, 'logs')
    APP_LOG_INFO = 'info.application.log'
    APP_LOG_ERROR = 'error.application.log'
    APP_LOG_SIZE = 4 * 1024 * 1024
    APP_LOG_FORMATTER = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    APP_ITEMS_PER_PAGE = 20
    APP_ITEMS_PER_PAGE_LG = 200
    APP_UPLOAD_FOLDER = os.path.join(APP_DIR, 'uploads')
    APP_COURSE_MAX_DURATION = 180
    APP_QRCODE_MAX_DURATION = 240
    APP_QRCODE_MIN_INTERVAL = 600

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfiguration(Configuration):
    DEBUG = True


class TestingConfiguration(Configuration):
    TESTING = True


class ProductionConfiguration(Configuration):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration,
    'production': ProductionConfiguration,
    'default': DevelopmentConfiguration
}
