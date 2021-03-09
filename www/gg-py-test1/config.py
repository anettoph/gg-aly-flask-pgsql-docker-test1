import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'LDnEDefh&4832gvFjkrfg87^&$#GYGF743fh'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@postgres:5432/test1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    PAGE_ROWS_COUNT = 5 # Количество записей в списке аккаунтов

