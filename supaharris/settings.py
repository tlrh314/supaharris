"""
Django settings for supaharris project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')iby(xl09u$43n!fd@nr67=-bwsfd$j(-41(f514dkdy(qhm*9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [u'127.0.0.1', u'localhost' ]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'catalogue.apps.CatalogueConfig',
    'django_forms_bootstrap',
    'crispy_forms',
    'bootstrap_themes',
    'django_tables2',
    'django_extensions',
    'freeze',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'supaharris.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'supaharris.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './'

#the absolute path where to store the .zip and the html files
#default value is a folder named 'freeze' located as sibling of 'settings.MEDIA_ROOT'
FREEZE_ROOT = '/home/eb0025/freeze/'

#tells 'freeze' if the urls should be fetched using https instead of http protocol (only if FREEZE_SITE_URL is not defined)
FREEZE_USE_HTTPS = False

#the site-url to crawl, if not specified it will be autodetected using the sites app
#FREEZE_SITE_URL = 'http://localhost:8000/'

#the base-url for all links relative to root '/'
#useful if the generated static site will run in a specific folder which is not the document-root
FREEZE_BASE_URL = None

#if True 'freeze' will convert all absolute urls to relative urls
#useful if the generated static site will run locally (file://) or in an unknown folder which is not the document-root (only if FREEZE_BASE_URL is not defined)
FREEZE_RELATIVE_URLS = True

#if True 'freeze' will inject a script at the end of each page
#which will force hrefs like 'path/' to 'path/index.html' (only if the site is running under file://)
#useful if the generated static site will run locally (requires FREEZE_RELATIVE_URLS set to True) to prevent local directory index
FREEZE_LOCAL_URLS = True

#if True 'freeze' will fetch each url founded in sitemap.xml
FREEZE_FOLLOW_SITEMAP_URLS = False

#if True 'freeze' will follow and fetch recursively each link-url founded in each page
FREEZE_FOLLOW_HTML_URLS = True

#if true 'freeze' will send an email to managers containing the list of all invalid urls (404, 500, etc..)
FREEZE_REPORT_INVALID_URLS = False

#the invalid urls email report subject
FREEZE_REPORT_INVALID_URLS_SUBJECT = '[freeze] invalid urls'

#if True the generated site will contain also the MEDIA folder and ALL its content
FREEZE_INCLUDE_MEDIA = False
#elif the value is a list or tuple only the specified directories will be included
#REEZE_INCLUDE_MEDIA = ('cache', 'images', 'videos', )

#if True the generated site will contain also the STATIC folder and ALL its content
FREEZE_INCLUDE_STATIC = True
#elif the value is a list or tuple only the specified directories will be included
FREEZE_INCLUDE_STATIC = ('catalogue/static', )

#if True the generated site will be zipped, the *.zip file will be created in FREEZE_ROOT
FREEZE_ZIP_ALL = False

#the name of the zip file created
FREEZE_ZIP_NAME = 'freeze'

#The request headers to use during the get requests that scrape the site
#can be used to set Authentication headers, by default sets the user-agent
FREEZE_REQUEST_HEADERS = {'user-agent': 'django-freeze'}

