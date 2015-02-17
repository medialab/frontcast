# //
# //
# //
# //     ______     ______     ______     ______     ______     __   __   ______     ______    
# //    /\  __ \   /\  == \   /\  ___\   /\  ___\   /\  == \   /\ \ / /  /\  ___\   /\  == \   
# //    \ \ \/\ \  \ \  __<   \ \___  \  \ \  __\   \ \  __<   \ \ \'/   \ \  __\   \ \  __<   
# //     \ \_____\  \ \_____\  \/\_____\  \ \_____\  \ \_\ \_\  \ \__|    \ \_____\  \ \_\ \_\ 
# //      \/_____/   \/_____/   \/_____/   \/_____/   \/_/ /_/   \/_/      \/_____/   \/_/ /_/ 
# //
# //
# //                                       *       +
# //                            *     '                  |
# //                              ()    .-.,-"``"-.    - o -
# //                                    '=/_       \     |
# //                                 *   |::'=._    ;      '
# //                            '         \::.  `=./`,   '
# //                              +    .   '-::..-'``'    *
# //                          jgs   O    *     .       +  .
# //                                   *     .       +
# //
# //
# //  ---
# //
# """
# Django settings for observer project.

# For more information on this file, see
# https://docs.djangoproject.com/en/1.7/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/1.7/ref/settings/
# """

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, local_settings, logging
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'glue',
    'observer'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'observer.urls'

WSGI_APPLICATION = 'observer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = local_settings.DATABASES

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'dist')
STATIC_URL = '/static/'

LOCALE_PATHS = (
  os.path.join(BASE_DIR, 'locale'),
)

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'client'),
)

TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'client'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s.%(funcName)s(%(lineno)d) %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'glue':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/glue.log'),
            'maxBytes': '16777216', # 16 megabytes
            'formatter': 'verbose'
        },
        'api':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/api.log'),
            'maxBytes': '16777216', # 16 megabytes
            'formatter': 'verbose'
        },
        'ldap':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/ldap.log'),
            'maxBytes': '16777216', # 16 megabytes
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['ldap'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# biblib
BIBLIB_ENDPOINT = local_settings.BIBLIB_ENDPOINT

# ldap
#import ldap
#from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# Baseline configuration.
AUTH_LDAP_SERVER_URI = local_settings.AUTH_LDAP_SERVER_URI
AUTH_LDAP_USER_DN_TEMPLATE = local_settings.AUTH_LDAP_USER_DN_TEMPLATE # something like "uid=%(user)s,ou=<Users>,o=<domain name>,c=<fr>"

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'observer.ldap.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)



try:
    from .local_settings import *
except ImportError:
    pass
