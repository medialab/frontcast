
DB_BACKEND	= 'django.db.backends.sqlite3'
DB_NAME	= '/path/to/frontcast/sqlite/frontcast.db'
DB_USER = ''
DB_PASS = ''
DB_HOST = ''
DB_PORT	= ''

# LDAP configuration
AUTH_LDAP_SERVER_URI = ""
AUTH_LDAP_USER_DN_TEMPLATE = ""

MEDIA_ROOT = '/path/to/frontcast/media'
SECRET_KEY = 'secret very secret key'

TEMPLATE_DIRS = (
	'/path/to/frontcast/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_DIRS = (
    '/path/to/frontcast/static',
)

STATIC_ROOT = '/path/to/frontcast/static/assets'
STATIC_URL = '/frontcast/static/'

LOCALE_PATHS = (
	'/path/to/frontcast/locale',
)

LANGUAGES = (
	('it', 'Italian'),
    ('en', 'English'),
    ('fr', 'French'),
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

GLUE_LOG_PATH = '/path/to/frontcast/logs/glue.log'
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
