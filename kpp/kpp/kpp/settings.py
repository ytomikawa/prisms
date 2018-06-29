import os
from kpp.settings_common import *

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'systemtrade',
        'USER': 'root',
        'PASSWORD': 'kabukabu',
        'HOST': 'systemtrade.cag3kcssghgq.ap-northeast-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}


# directory of KABU+ CSV files
KABUPLUS_DIRECTORY = 'Y:\kabu.plus\csv'