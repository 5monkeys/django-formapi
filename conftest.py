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
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MEDIA_ROOT='/tmp/formapi/',
        MEDIA_PATH='/media/',
        ROOT_URLCONF='formapi.tests.urls',
        DEBUG=True,
        TEMPLATE_DEBUG=True,
    )
    return settings
