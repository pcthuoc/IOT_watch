# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string
from dotenv import load_dotenv
from unipath import Path
import dj_database_url

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# settings.py
ZALO_TTS_API_KEY = "r4OQbtCrRbldRpM15AUEHGk3Q5BrZ857"
MQTT_BROKER_HOST = os.getenv('MQTT_BROKER_HOST', '103.252.136.73')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'IOT/#')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'admin')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'admin')
TIME_SAVE = os.getenv('TIME_SAVE', 5)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG   = os.getenv('DEBUG', False)
DEVEL   = os.getenv('DEVEL', False)
SERVER  = os.getenv('DEVEL', '127.0.0.1')

# load production server from .env
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'channels',
    'daphne',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    
    'app',  # Enable the inner appclear
    'sensors',
    'alert',
    'reminder',
    'mqtt_call'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"   # Route defined in app/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "core/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
ASGI_APPLICATION = "core.asgi.application"
REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(str(REDIS_HOST), int(REDIS_PORT))]

        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'  # Đặt múi giờ là múi giờ TP.HCM


USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(CORE_DIR, 'media')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'core/static'),
)
#############################################################
#############################################################
