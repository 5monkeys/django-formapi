# coding=utf-8
import django


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
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        MEDIA_ROOT='/tmp/formapi/',
        MEDIA_PATH='/media/',
        ROOT_URLCONF='formapi.tests.urls',
        SECRET_KEY='qw%34231=hygcq4jqs&#b%9*8v(0weqzxf#$@$!@#!@#!@#-6we',
        DEBUG=True,
        TEMPLATE_DEBUG=True,
    )

    if hasattr(django, 'setup'):
        django.setup()

    return settings
