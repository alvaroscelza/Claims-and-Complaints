import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path
import environ

# Meta
APP_NAME = 'Claims and Complaints'
APP_DESCRIPTION = _(
    'This project is a Django application that allows users to create claims and complaints about '
    'different companies.'
)

# Base Settings
BASE_DIR = Path(__file__).parent.parent

env = environ.Env(
    IS_PRODUCTION=(bool, True),
    SECRET_KEY=(str),
    LANGUAGE_CODE=(str, 'es'),
    ALLOWED_HOSTS=(str),
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(int, 0),
    EMAIL_USERNAME=(str),
    EMAIL_PASSWORD=(str),
)
environ.Env.read_env(BASE_DIR / '.env')


# Enviroment Variables
IS_PRODUCTION = env('IS_PRODUCTION')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',') if IS_PRODUCTION else ['*']

# Configured Values
DEBUG = not IS_PRODUCTION


# Django Base Configurations
ROOT_URLCONF = 'config.urls'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S.%f',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.TemplateHTMLRenderer'],
    'EXCEPTION_HANDLER': 'applications.utils.exception_handler',
    'PAGE_SIZE': 10,
}
if IS_PRODUCTION and not env('DATABASE_NAME'):
    raise Exception('Postgres Database not defined for production, please check .env')

if not IS_PRODUCTION and not env('DATABASE_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT'),
        }
    }
# Django Security Configurations
CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost").split(",")


# region INSTALLED_APPS
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
LOCAL_APPS = ['users', 'applications.apps.CoreConfig']
EXTERNAL_APPS = [
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
]
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS
# endregion INSTALLED_APPS

# region Internationalization
LANGUAGE_CODE = env('LANGUAGE_CODE')
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGES = [('es', _('Spanish')), ('en-us', _('English (US)'))]
TIME_ZONE = 'America/Montevideo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# endregion

# region Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_storage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# endregion
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'generic_helper': 'templatetags.custom_tags',
            },
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'

# Auth
AUTH_USER_MODEL = 'users.User'  # Set default user model
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Email Variables
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_FROM_NAME = 'Claims & Complaints'  # The name users will see in their inbox

# Branding
BRAND_NAME = 'Claims & Complaints'
SITE_URL = 'http://127.0.0.1'
