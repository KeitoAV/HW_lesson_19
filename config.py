import os


class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'movies.db')
