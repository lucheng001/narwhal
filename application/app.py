# -*- coding: utf-8 -*-

import logging
import os
from flask import Flask
from .configuration import config
from .extensions import csrf, lm, db


__all_ = ['create_app']


def create_app(config_name):
    """Creates the app."""

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    configure_extensions(app)
    configure_blueprints(app)
    configure_template_filters(app)
    configure_template_global_variables(app)
    configure_context_processors(app)
    configure_before_handlers(app)
    configure_error_handlers(app)
    configure_logging(app)

    return app


def configure_extensions(app):
    """Configures the extensions."""

    csrf.init_app(app)
    db.init_app(app)

    lm.init_app(app)
    lm.session_protection = 'strong'
    lm.login_view = 'bpAuth.login'
    lm.login_message = u'请登录'
    lm.login_message_category = 'error'
    lm.needs_refresh_message = u'请重新登录'
    lm.needs_refresh_message_category = 'error'

    @lm.user_loader
    def load_user(user_id):
        from .models import User
        try:
            user = User.get(User.id == int(user_id))
        except User.DoesNotExist:
            user = None
        return user


def configure_blueprints(app):
    from .main import bpMain as mainBlueprint
    app.register_blueprint(mainBlueprint)

    from .auth import bpAuth as authBlueprint
    app.register_blueprint(authBlueprint, url_prefix='/auth')

    from .user import bpUser as userBlueprint
    app.register_blueprint(userBlueprint, url_prefix='/user')

    from .course import bpCourse as courseBlueprint
    app.register_blueprint(courseBlueprint, url_prefix='/course')


def configure_context_processors(app):
    """Configures the context processors."""
    import datetime

    @app.context_processor
    def inject_globals_variables():
        return dict(
            gServerNow=datetime.datetime.now(),
            gServerToday=datetime.date.today()
        )


def configure_before_handlers(app):
    """Configures the before request handlers."""
    pass


def configure_template_filters(app):
    """Configures the template filters."""
    pass


def configure_template_global_variables(app):
    """Configures the template filters."""
    from .constants import CntRoles, CntPermission, CntSyllabusYear, CntDepartment, CntCourseMaterials
    app.jinja_env.globals['cRoles'] = CntRoles
    app.jinja_env.globals['cPermission'] = CntPermission
    app.jinja_env.globals['cDepartment'] = CntDepartment
    app.jinja_env.globals['cSyllabusYear'] = CntSyllabusYear
    app.jinja_env.globals['cCourseMaterials'] = CntCourseMaterials

def configure_error_handlers(app):
    """Configures the error handlers."""
    pass


def configure_logging(app):
    """Configures logging."""

    from logging.handlers import RotatingFileHandler

    logsFolder = app.config['APP_LOG_DIR']
    formatter = logging.Formatter(app.config['APP_LOG_FORMATTER'])

    infoLog = os.path.join(logsFolder, app.config['APP_LOG_INFO'])
    infoFileHandler = RotatingFileHandler(
        infoLog,
        maxBytes=app.config['APP_LOG_SIZE'],
        backupCount=10
    )
    infoFileHandler.setLevel(logging.INFO)
    infoFileHandler.setFormatter(formatter)
    app.logger.addHandler(infoFileHandler)

    errorLog = os.path.join(logsFolder, app.config['APP_LOG_ERROR'])
    errorFileHandler = RotatingFileHandler(
        errorLog,
        maxBytes=app.config['APP_LOG_SIZE'],
        backupCount=10
    )
    errorFileHandler.setLevel(logging.ERROR)
    errorFileHandler.setFormatter(formatter)
    app.logger.addHandler(errorFileHandler)



