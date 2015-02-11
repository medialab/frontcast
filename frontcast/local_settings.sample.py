import os

FRONTCAST_HOME = os.path.dirname(os.path.dirname(__file__))

DB_BACKEND	= 'django.db.backends.sqlite3'
DB_NAME	= '%s/sqlite/frontcast.db' % FRONTCAST_HOME
DB_USER = ''
DB_PASS = ''
DB_HOST = ''
DB_PORT	= ''

# LDAP configuration
AUTH_LDAP_SERVER_URI = ""
AUTH_LDAP_USER_DN_TEMPLATE = ""

# media and storage root differs: media is the path where uploaded stuff goes, storage allow FTP access
MEDIA_ROOT = '%s/media' % FRONTCAST_HOME
STORAGE_ROOT = '/external%s/storage/public' % FRONTCAST_HOME
STORAGE_ROOT_PROTECTED = '/external%s/storage/protected' % FRONTCAST_HOME # available only for logged in sessions
STORAGE_ROOT_PUBLIC = MEDIA_ROOT

SECRET_KEY = 'secret very secret key'

TEMPLATE_DIRS = (
	'%s/templates' % FRONTCAST_HOME,
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_DIRS = (
    '%s/static' % FRONTCAST_HOME,
)

STATIC_ROOT = '%s/static/assets' % FRONTCAST_HOME
STATIC_URL = '/frontcast/static/'

LOCALE_PATHS = (
	'%s/locale' % FRONTCAST_HOME,
)

LANGUAGES = (
	('it', 'Italian'),
    ('en', 'English'),
    ('fr', 'French'),
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

GLUE_LOG_PATH = '%s/logs/glue.log' % FRONTCAST_HOME
GLUE_ACCESS_DENIED_URL ='/api/access-denied/'


ALCHEMY_API_KEY = 'if any'


# describe which affilitation are allowed
WALT_AFFILIATIONS = [
  {
    'name': 'Sciences-Po'
  }
]

WALT_ROLES = [
  {
    'name': 'Student'
  },
  {
    'name': 'Professor'
  }
]


BIBLIB_ENDPOINT = None

EMAIL_HOST = 'smtp.domain.com'
EMAIL_PORT = 25

# IF frontcast is used by nginx servers - set to True = ENABLE STREAMING. Otherwise leave this value to False
ENABLE_XACCEL = False