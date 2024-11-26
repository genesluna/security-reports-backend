import os

import django
from django.conf import settings

# Set the default Django settings module
os.environ["DJANGO_SETTINGS_MODULE"] = "conftest"


def pytest_configure():
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.admin",
            "src.report",
        ],
        SECRET_KEY="test_secret_key",
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        ROOT_URLCONF="src.urls",
    )
    django.setup()
