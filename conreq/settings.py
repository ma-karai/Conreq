"""
Django settings for Conreq project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import ast
import os

from django.core.management.utils import get_random_secret_key

from conreq.core import log


# Settings Helper Function
def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except Exception as exception:
            log.handler(
                str(exception),
                log.WARNING,
                __logger,
            )
    return default_value


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env("CONREQ_DEBUG", True)

# Logging for the settings configuration
__logger = log.get_logger("conreq.settings")
log.configure(__logger, log.DEBUG)
log.configure(log.get_logger(), log.INFO)
if DEBUG:
    log.console_stream(log.get_logger(), log.WARNING)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("DATA_DIR")
if not DATA_DIR:
    # log.handler(
    #     "DATA_DIR not configured, using default data directory.",
    #     log.WARNING,
    #     __logger,
    # )
    DATA_DIR = BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
# TODO: Store secret key in database
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    log.handler(
        "SECRET_KEY not configured, using a random temporary key.",
        log.WARNING,
        __logger,
    )
    SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "conreq.apps.discover",
    "conreq.apps.more_info",
    "conreq.apps.login",
    "conreq.apps.search",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": os.path.join(DATA_DIR, "cache"),
        "TIMEOUT": 300,  # Django setting for default timeout of each key.
        "SHARDS": 8,  # Number of db files to create
        "DATABASE_TIMEOUT": 0.010,  # 10 milliseconds
        "OPTIONS": {"size_limit": 2 ** 30},  # 1 gigabyte
    }
}

ROOT_URLCONF = "conreq.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "conreq.wsgi.application"
ASGI_APPLICATION = "conreq.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(DATA_DIR, "db.sqlite3"),
        "OPTIONS": {
            "timeout": 30,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
