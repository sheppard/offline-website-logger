SECRET_KEY = '1234'
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'owl',
    'tests.test_app',
)
MIDDLEWARE_CLASSES = tuple()
ROOT_URLCONF = 'tests.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
USE_TZ = True
