"""
Django settings for aoasurveys project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_assets',
    'frame',
    'aoasurveys',
    'aoasurveys.manager',
    'aoasurveys.reports',
    'aoasurveys.aoaforms',
    'aoasurveys.cpanel',
    'forms_builder.forms',
)

MIDDLEWARE_CLASSES = (
    'frame.middleware.RequestMiddleware',
    'frame.middleware.UserMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'frame.backends.FrameUserBackend',
)

TEMPLATE_LOADERS = (
    'frame.loaders.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'aoasurveys.urls'

WSGI_APPLICATION = 'aoasurveys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Custom fields
# CHECKBOX = 4
# CHECKBOX_MULTIPLE = 5
# SELECT = 6
# SELECT_MULTIPLE = 7
# RADIO_MULTIPLE = 8

LOCALIZEDSTRING = 100
LOCALIZEDTEXTAREA = 101

FORMS_BUILDER_EXTRA_FIELDS = (
    (LOCALIZEDSTRING, "aoasurveys.aoaforms.fields.LocalizedStringField",
     "LocalizedStringField"),
    (LOCALIZEDTEXTAREA, "aoasurveys.aoaforms.fields.LocalizedTextAreaField",
     "LocalizedTextAreaField"),
)

# FORMS_BUILDER_EXTRA_WIDGETS = (
#     (RADIO_MULTIPLE, "aoasurveys.aoaforms.widgets.LocalizedRadioSelect"),
# )

LOCALIZED_LANGUAGES = (
    "English",
    "Russian"
)
LOCALIZED_LANGUAGES_ABBR = ('en', 'ru')
DEFAULT_LANGUAGE = 'en'
FORMS_BUILDER_UPLOAD_ROOT = os.path.join(BASE_DIR, 'forms')

# Custom settings
SITE_ID = 1
FORMS_BUILDER_USE_SITES = False

CUSTOM_JS = {}

try:
    from local_settings import *
except ImportError:
    pass
