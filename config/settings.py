import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
APP_NAME = 'Claims and Complaints'
APP_DESCRIPTION = _('This project is a Django application that allows users to create claims and complaints about '
                    'different companies.')
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}]
BASE_DIR = Path(__file__).parent.parent
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
DEBUG = os.getenv('DEBUG', False)
# region INSTALLED_APPS
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
LOCAL_APPS = ['applications.apps.CoreConfig', 'applications.button']
EXTERNAL_APPS = ['rest_framework', 'crispy_forms', 'crispy_bootstrap5']
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS
# endregion INSTALLED_APPS
# region Internationalization
LANGUAGE_CODE = 'es'
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGES = [('es', _('Spanish'))]
TIME_ZONE = 'America/Montevideo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# endregion
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
    'PAGE_SIZE': 10
}
ROOT_URLCONF = 'config.urls'
SECRET_KEY = os.getenv('SECRET_KEY')
# region Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_storage')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# endregion
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
