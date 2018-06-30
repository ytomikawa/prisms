from kpp.settings_common import *

ALLOWED_HOSTS = ['kabu.windy.ac', '13.115.25.5']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

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
KABUPLUS_DIRECTORY = '/'
