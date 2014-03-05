# coding=utf-8


def pytest_configure():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'formapi',
            'formapi.tests',
        ],
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        MEDIA_ROOT='/tmp/formapi/',
        MEDIA_PATH='/media/',
        ROOT_URLCONF='formapi.tests.urls',
        DEBUG=True,
        TEMPLATE_DEBUG=True,
    )
    return settings
