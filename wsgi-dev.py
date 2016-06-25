# -*- coding: utf-8 -*-

from application import create_app

app = create_app('development')

if __name__ == '__main__':
    # app.logger.info('narwhal started')
    app.run()

