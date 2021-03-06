"""
Django settings.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from fao_case_list.general_settings import *  # noqa


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = "$secret_key"

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = $debug  # True or False

ALLOWED_HOSTS = ["$host"]  # List of hosts, e. g. ["*"]

WSGI_APPLICATION = "fao_case_list_wsgi.application"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "deployment", "static"
)

MEDIA_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "deployment", "media"
)


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

$databases
