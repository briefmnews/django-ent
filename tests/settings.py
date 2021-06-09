SECRET_KEY = "dump-secret-key"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django_ent",
)


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

ENT_HDF_BASE_URL = "https://preprod.enthdf.fr/"
ENT_QUERY_STRING_TRIGGER = "sso_id"
