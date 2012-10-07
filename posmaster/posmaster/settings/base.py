import os.path
import dj_database_url

# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Database
DATABASES = {'default': dj_database_url.config()}

# I18N/L10N
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Site Config
SITE_ID = 1
SECRET_KEY = ''

# Media and Static files
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Templates
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
)

# Applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'poscore',
)
ROOT_URLCONF = 'posmaster.urls'
WSGI_APPLICATION = 'posmaster.wsgi.application'

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
