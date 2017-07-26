"""
Django settings for imagersite project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecrete')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ec2-50-112-40-8.us-west-2.compute.amazonaws.com', '127.0.0.1', 'localhost']

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'c.hud.imager@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PW')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'c.hud.imager@gmail.com'
SERVER_EMAIL = 'c.hud.imager@gmail.com'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imager_profile',
    'imagersite',
    'imager_images',
    'sorl.thumbnail',
    'taggit',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imagersite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'imagersite/imager_images/templates/imager_images'),
                 os.path.join(BASE_DIR, 'imagersite/imagersite/templates/imagersite')],
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

WSGI_APPLICATION = 'imagersite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_db'
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REGISTRATION_OPEN = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        '/var/www/static/'
    ]

    MEDIA_URL = '/MEDIA/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')
else:
    AWS_STORAGE_BUCKET_NAME = 'chris-django-imager'
    AWS_ACCESS_KEY_ID = os.environ.get('IAM_USER_ACCESS_KEY_ID')

    AWS_SECRET_ACCESS_KEY = os.environ.get('IAM_USER_SECRET_ACCESS_KEY')

    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(
        AWS_STORAGE_BUCKET_NAME
    )

    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'imagersite.custom_storages.StaticStorage'
    STATIC_URL = 'https://{}/{}/'.format(
        AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION
    )

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'imagersite.custom_storages.MediaStorage'
    MEDIA_URL = 'https://{}/{}/'.format(
        AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION
    )
