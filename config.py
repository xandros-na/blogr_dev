import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 's3cr3t_h4h4'
    DATABASE_URI = os.path.join(basedir, 'blogr.db')
    USERNAME='admin'
    PASSWORD='asdf'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
        }
