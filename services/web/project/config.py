import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = os.environ['CACHE_TYPE']
    CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
