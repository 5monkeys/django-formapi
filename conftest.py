import django


def pytest_configure():
    import logging

    logging.basicConfig(level=logging.ERROR)

    from django.conf import settings

    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.admin",
            "django.contrib.sessions",
            "formapi",
            "formapi.test_app",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        MIDDLEWARE_CLASSES=[],
        MEDIA_ROOT="/tmp/formapi/",
        MEDIA_PATH="/media/",
        ROOT_URLCONF="formapi.test_app.urls",
        SECRET_KEY="monkey",
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        TEMPLATES=[
            {
                "APP_DIRS": True,
                "BACKEND": "django.template.backends.django.DjangoTemplates",
            },
        ],
    )

    if django.VERSION >= (1, 7):
        django.setup()

    return settings
