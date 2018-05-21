# -*- coding: utf-8 -*-
"""
Django settings for ask_price_project project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import sys
from corsheaders.defaults import default_headers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

AUTH_USER_MODEL = 'account.User'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1k9paff%2pkn6e-4s()b^h)h0jjhqn5wy@_t5b5(h7m=#t+5wg'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = []

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

# Application definition


EMAIL_HOST = 'xxx.163.com'  # SMTP地址 smtp.域名
EMAIL_PORT = 465  # SMTP端口
EMAIL_HOST_USER = 'xxxx@163.com'  # 邮箱
EMAIL_HOST_PASSWORD = '123456'  # 邮箱密码
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'xxxx@163.com'
# EMAIL_TIMEOUT = 3

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'oauth2_provider',

    'corsheaders',   # 跨域
    'rest_framework',
    'rest_framework.authtoken',
    'common',
    'apps.account',
    'apps.hospital',
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.RegionMiddleware'
]


ROOT_URLCONF = 'ask_price.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ask_price.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-HANS'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/").replace('\\', '/')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/").replace('\\', '/')

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

HEALTHY_DOC_BASE_URL = 'https://123456.com/'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        # 'rest_framework.permissions.DjangoObjectPermissions',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'ALLOWED_VERSIONS': None,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter',
                                'rest_framework.filters.SearchFilter',),
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'NON_FIELD_ERRORS_KEY': 'errors',
    # datetime数据输出格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',

    # 请求频率设置
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',

        # 'common.throttling.ChargeRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '300/minute',
        'user': '600/minute',
        'charge': '20/minute',
        'feedback': '10/minute',
        'group_check': '6/minute',
    }
}


# 单元测试时, 跳过migrate, 极 的提升测试运 效率
# 具体可以查看
# https://simpleisbetterthancomplex.com/tips/2016/08/19/django-tip-12-disabl ing-migrations-to-speed-up-unit-tests.html
# https://stackoverflow.com/questions/36487961/django-unit-testing-taking-a- very-long-time-to-create-test-database
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING:
    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return "notmigrations"


    MIGRATION_MODULES = DisableMigrations()

