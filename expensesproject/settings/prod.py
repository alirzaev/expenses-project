import dj_database_url

from .defaults import *

_MAX_CONN_AGE = 600

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(conn_max_age=_MAX_CONN_AGE)
}

SECRET_KEY = os.environ['SECRET_KEY']
