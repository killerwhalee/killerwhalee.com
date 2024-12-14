"""
Django Configuration

This is the settings for killerwhalee.com.

Configuration which needs to be secured are separated using environment variable.
Define your own environment variable file to configure those settings.

Also it supports default value for those, which is safe to use.
But please remind that default value is only for development.

Configured by killerwhalee

"""

from pathlib import Path
import dotenv, os

# Load Environment Variables

dotenv.load_dotenv()

# Host Name

HOST_NAME = os.environ.get("HOST_NAME", "localhost")


# Base Directory

BASE_DIR = Path(__file__).resolve().parent.parent


# Secret Key for Django

from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", 0)))


# Allowed Hosts

ALLOWED_HOSTS = [f".{HOST_NAME}", "localhost", "127.0.0.1"]


# Application Definition

INSTALLED_APPS = [
    # Third-party applications
    "daphne",
    # System built-in applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # User defined applications
    "home",
    "user",
    # Project applications
    "projects.interactive",
    "projects.omok",
    "projects.id221",
]


# Middleware Setting

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Url Configuration

ROOT_URLCONF = "core.urls"


# Templates Setting

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["_templates"],
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


# WSGI Setting

WSGI_APPLICATION = "core.wsgi.application"


# ASGI Setting

ASGI_APPLICATION = "core.asgi.application"


# Channel Layers

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# Database Setting
# Default is SQLite3. Override the setting for other option.

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DJANGO_DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DJANGO_DATABASE_USER", "user"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "password"),
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_DATABASE_PORT", "5432"),
    }
}


# Customized User Model

AUTH_USER_MODEL = "user.User"


# Password Validation
#
# 1. Password must not be too similar with other user variable.
# 2. Password should be at least 8 characters.
# 3. It is not allowed to use common vulnerable passwords.
# 4. It is not allowed only to use number for password.

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


# Registration
# Redirect to Root for default.

LOGIN_REDIRECT_URL = "home:index"

LOGOUT_REDIRECT_URL = "home:index"


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

DATE_FORMAT = "Y.m.d"

DATETIME_FORMAT = "Y.m.d h:i A"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files

STATIC_URL = "static/"

if DEBUG:
    STATICFILES_DIRS = ["_static"]

else:
    STATIC_ROOT = BASE_DIR / "_static"


# User Media

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "_media"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging
# * Logging setting is now in progress.
# * Setting would change in near future.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "_logs/server.log",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 256,
            "formatter": "standard",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
}
