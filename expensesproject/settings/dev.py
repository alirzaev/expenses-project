import django_heroku

from .defaults import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

SECRET_KEY = '_ajlm!6v=$2tfao+1!7r!+)dg&g2c0gp=j!9c%dbnol!&60i9k'

django_heroku.settings(locals())
