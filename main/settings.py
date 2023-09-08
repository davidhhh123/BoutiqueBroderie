

import os
from datetime import datetime, timedelta



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0%idv*_kqa2u4i^_vkh*335d+a^z%(bo=sca=x$(ju@&+=!%8g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    
    'mathfilters',
    'store',
    'froala_editor',
    'debug_toolbar',
    


    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_globals.middleware.Global',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'


DEFAULT_CURRENCY_CODE = 'ENG'
RATE_USD = 1
RATE_AMD = 1
RATE_RUR = 1
CURRENCIES_RATES={
    'USD': RATE_USD,
    'RUR': 2,
    'AMD': 1,
    'EUR': 4,
    }
RATES=1


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False
DECIMAL_SEPARATOR = '.'

USE_TZ = True
LANGUAGES = (
   
    ('en', 'English'),
   
    ('hy', "Armenian"),
    ('ru', "Russian")
)
CURRENCIES = (
   
    ('USD', '$'),
   
    ('RUR', "r"),
    
)



SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_URL = '/assets/'
if DEBUG:
    STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'assets')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.boutiquebroderie.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '_mainaccount@boutiquebroderie.com'
EMAIL_HOST_PASSWORD = 'zJP*cIz3|rIr'
DEFAULT_FROM_EMAIL = '_mainaccount@boutiquebroderie.com'
EMAIL_USE_SSL = True


if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)