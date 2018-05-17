# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from .base import *

DEBUG = False

# INSTALLED_APPS += ('rest_framework_swagger',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': BASE_DIR + '/ask_price/settings/prod.cnf',
        },
        'ATOMIC_REQUESTS': True,
    }
}

# 跨域配置
CORS_ORIGIN_WHITELIST = ['https://quot.touchealth.com.cn']
CORS_URLS_REGEX = r'^/api/manage/.*$'

LOGGING_PREFIX = 'prod'

ALLOWED_HOSTS = ['quot.touchealth.com.cn',]

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        #         'mail_admins': {
        #             'level': 'ERROR',
        #             'class': 'django.utils.log.AdminEmailHandler',
        #             'include_html': True,
        #         },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志输出文件
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_all.log'),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 100,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_error.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 100,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_request.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 100,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/',
                                     LOGGING_PREFIX + '_script.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 100,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['scprits_handler', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'scripts': {
            'handlers': ['scprits_handler', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # 这写的应该是项目下的包名,而不是项目名
        'apps': {
            'handlers': ['default', 'console'],
            'level': 'INFO',  # 正式环境修改为INFO
            'propagate': False,
        },
        'common': {
            'handlers': ['default', 'console'],
            'level': 'INFO',  # 正式环境修改为INFO
            'propagate': False,
        },
    }
}