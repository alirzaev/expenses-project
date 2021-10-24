import os

import dj_database_url

from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default'] = dj_database_url.config(conn_max_age=600)

SECRET_KEY = os.environ['SECRET_KEY']
