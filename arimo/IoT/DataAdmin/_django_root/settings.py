import os
from ruamel import yaml
import sys


# check if running on Linux cluster or local Mac
_ON_LINUX_CLUSTER = sys.platform.startswith('linux')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(_PROJECT_DIR)


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not _ON_LINUX_CLUSTER


ALLOWED_HOSTS = \
    ['.arimo.com', '.elasticbeanstalk.com'] \
    if _ON_LINUX_CLUSTER \
    else ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    # Django-AutoComplete-Light: add to INSTALLED_APPS BEFORE django.contrib.admin
    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_filters',

    'silk',

    'arimo.IoT.DataAdmin.base',
    'arimo.IoT.DataAdmin.PredMaint',
    'arimo.IoT.DataAdmin.tasks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'silk.middleware.SilkyMiddleware'
]

ROOT_URLCONF = 'arimo.IoT.DataAdmin._django_root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'arimo.IoT.DataAdmin._django_root.wsgi.application'


# Database
_CONFIG_FILE_NAME = 'db.yaml'
_CONFIG_FILE_PATH = os.path.join(_PROJECT_DIR, _CONFIG_FILE_NAME)

try:
    _db_creds = yaml.safe_load(stream=open(_CONFIG_FILE_PATH, 'r'))['db']

except Exception as err:   # https://stackoverflow.com/questions/50879668/python-setup-py-some-files-are-missing
    print('*** {} ***'.format(err))

    _db_creds = \
        dict(host=None,
             user=None,
             password=None,
             db_name=None)

DATABASES = \
    dict(default=
            dict(ENGINE='django.db.backends.postgresql', PORT='5432',
                 HOST=_db_creds['host'],
                 USER='arimo', PASSWORD='arimoiscool',
                 NAME=_db_creds['db_name']))


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, '_static_files')
STATIC_URL = '/static/'


# Data Upload
DATA_UPLOAD_MAX_MEMORY_SIZE = 8388608   # 8 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000


# REST Framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.RemoteUserAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework_filters.backends.ComplexFilterBackend'   # RestFrameworkFilterBackend
    ]
}
