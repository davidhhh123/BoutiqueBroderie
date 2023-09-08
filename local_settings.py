SECRET_KEY = '0%idv*_kqa2u4i^_vkh*335d+a^z%(bo=sca=x$(ju@&+=!%8g'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DEBUG=True

EMAIL_*=""