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
            "django.contrib.messages",
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
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ],
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
                "OPTIONS": {
                    "context_processors": [
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                        "django.template.context_processors.request",
                    ],
                },
            },
        ],
    )

    django.setup()

    return settings
