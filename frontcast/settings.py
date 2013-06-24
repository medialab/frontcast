# Django settings for frontcast project.
import local_settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': local_settings.DB_BACKEND, # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': local_settings.DB_NAME,                      # Or path to database file if using sqlite3.
        'USER': local_settings.DB_USER,                      # Not used with sqlite3.
        'PASSWORD': local_settings.DB_PASS,                  # Not used with sqlite3.
        'HOST': local_settings.DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': local_settings.DB_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-it'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = local_settings.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = local_settings.STATIC_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = local_settings.STATIC_URL

# Additional locations of static files
STATICFILES_DIRS = local_settings.STATICFILES_DIRS

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = local_settings.SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'frontcast.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'frontcast.wsgi.application'

TEMPLATE_DIRS = local_settings.TEMPLATE_DIRS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'walt',
    'glue'

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
            'filename': local_settings.GLUE_LOG_PATH,
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
        'glue':{ # glue content management app
            'handlers': ['glue'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

LOGIN_URL = local_settings.LOGIN_URL
LOGOUT_URL = local_settings.LOGOUT_URL
GLUE_ACCESS_DENIED_URL = local_settings.GLUE_ACCESS_DENIED_URL


LOCALE_PATHS = local_settings.LOCALE_PATHS
LANGUAGES = local_settings.LANGUAGES


# BIBTEXT API 



# LDAP
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"

AUTH_LDAP_BIND_DN = "cn=django-agent,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "phlebotinum"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
# or perhaps:
# AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=users,dc=example,dc=com"

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=django,ou=groups,dc=example,dc=com",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=django,ou=groups,dc=example,dc=com"
AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_PROFILE_ATTR_MAP = {
    "employee_number": "employeeNumber"
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
}

AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
}

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600


# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
