from kpp.settings_common import *

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