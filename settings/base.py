import os
import sys

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()
env.read_env(str((environ.Path(__file__) - 1).path(".env")))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use the "apps" folder for our project apps
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# `env LC_CTYPE=C tr -dc "a-zA-Z0-9" < /dev/random | head -c 50; echo`
SECRET_KEY = env("SECRET_KEY", default="secret")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

CACHES = {"default": env.cache()}

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "filebrowser",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "tinymce",
    "django_filters",
    "rest_framework",
    "rest_framework_datatables",
    "silk",
    "about",
    "accounts",
    "catalogue",
]

SITE_ID = 1


MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # templates shared between apps
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

WSGI_APPLICATION = "settings.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# This makes sure static files are also found in the static folder
# These can then be used for multiple apps
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000

# Use a custom model for account management, which makes it much easier to
# extend the model later on.
AUTH_USER_MODEL = "accounts.UserModel"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:profile"
ADMIN_BCC = []

EMAIL_CONFIG = env.email_url("EMAIL_URL")
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = "info@supaharris.com"
SERVER_EMAIL = "info@supaharris.com"


# http://django-filebrowser.readthedocs.io/en/latest/settings.html
# FILEBROWSER_DIRECTORY = "/media/uploads"
FILEBROWSER_DEFAULT_PERMISSIONS = 0o644
FILEBROWSER_OVERWRITE_EXISTING = True
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg", ".gif", ".png", ".tif", ".tiff"],
    "Document": [],  # [".pdf",".doc",".rtf",".txt",".xls",".csv"],
    "Video": [],  # [".mov",".wmv",".mpeg",".mpg",".avi",".rm"],
    "Audio": [],  # [".mp3",".mp4",".wav",".aiff",".midi",".m4p"]
}
FILEBROWSER_ADMIN_VERSIONS = ["big"]  # "thumbnail", "small", "medium", "large"


# https://www.tinymce.com/docs/demo/full-featured/
TINYMCE_DEFAULT_CONFIG = {
    "selector": "textarea",
    "height": 500,
    "theme": "modern",
    "plugins": [
        "advlist autolink lists link image charmap print preview hr anchor pagebreak",
        "searchreplace wordcount visualblocks visualchars code fullscreen",
        "insertdatetime media nonbreaking save table contextmenu directionality",
        "emoticons template paste textcolor colorpicker textpattern imagetools codesample toc",
    ],
    "toolbar1": "undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
    "toolbar2": "print preview image | forecolor backcolor emoticons | codesample",
    "image_advtab": True,
    "templates": [
        {"title": "Test template 1", "content": "Test 1"},
        {"title": "Test template 2", "content": "Test 2"},
    ],
    "content_css": [
        "//fonts.googleapis.com/css?family=Lato:300,300i,400,400i",
        "//www.tinymce.com/css/codepen.min.css",
        "/static/css/main.css",
    ],
}
# TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_FILEBROWSER = True
TINYMCE_MINIMAL_CONFIG = {
    "selector": "textarea",
    "height": 80,
    "width": 500,
    "menubar": False,
    "statusbar": False,
    "elementpath": False,
    "plugins": [
        "link paste autolink code",
    ],
    "toolbar1": "undo redo | bold italic | bullist numlist outdent indent | link code",
    "toolbar2": "",
}


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework_datatables.filters.DatatablesFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework_datatables.pagination.DatatablesPageNumberPagination",
    "PAGE_SIZE": 50,
}


# Silky for profiling / monitoring the api response times
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True  # default is_staff=True; overwrite below
SILKY_PERMISSIONS = lambda user: user.is_superuser
SILKY_PYTHON_PROFILER = False
SILKY_PYTHON_PROFILER_BINARY = False
SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, "profiles")
# SILKY_MAX_REQUEST_BODY_SIZE = -1     # Silk takes anything <0 as no limit
# SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
# SILKY_INTERCEPT_PERCENT = 50 # log only 50% of requests
# SILKY_MAX_RECORDED_REQUESTS = 10**4  # garbage collection of old data
# SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10
SILKY_META = True  # to check the effect Silk itself has on response time


# Sentry for error reporting
SENTRY_DSN_API = env("SENTRY_DSN_API", default="")

sentry_sdk.init(
    dsn=SENTRY_DSN_API,
    integrations=[DjangoIntegration()],
)


# To retrieve data from ADS api
ADS_API_TOKEN = env("ADS_API_TOKEN", default="")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


if DEBUG:
    PREPEND_WWW = False

    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    DEBUG_TOOLBAR_CONFIG = {
        "JQUERY_URL": "",
    }

    # mariadb:10.4 seems to have wait_timeout = 600 in /etc/mysql/my.cnf
    # so we set our CONN_MAX_AGE to something smaller than that
    DATABASES["default"]["CONN_MAX_AGE"] = 60
