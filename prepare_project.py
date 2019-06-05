"""
Small helper script to create settings file and WSGI file from templates.
"""
import os
from string import Template
from textwrap import dedent

from django.utils.crypto import get_random_string


DATABASES_DEVELOPMENT = dedent(
    """
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'db.sqlite3'
            ),
        }
    }
    """
).strip()

DATABASES_PRODUCTION = dedent(
    """
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'fao_case_list',
            'USER': 'fao_case_list',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
    """
).strip()


def create_settings():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    new_settings_file_path = os.path.join(base_dir, 'fao_case_list_settings.py')
    if not os.path.exists(new_settings_file_path):
        default_settings_file_path = os.path.join(base_dir, 'fao_case_list_settings.py.tpl')
        with open(default_settings_file_path) as default_settings_file:
            secret_key = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
            host = os.environ.get('FAO_CASE_LIST_HOST')
            databases = DATABASES_PRODUCTION if host else DATABASES_DEVELOPMENT
            context = dict(
                secret_key=secret_key,
                debug=not host,
                host=host if host else '*',
                databases=databases,
            )
            settings = Template(default_settings_file.read()).substitute(**context)
            with open(new_settings_file_path, 'w') as new_settings_file:
                new_settings_file.write(settings)
        print('Settings file {} successfully created.'.format(new_settings_file_path))


def create_wsgi():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    new_wsgi_file_path = os.path.join(base_dir, 'fao_case_list_wsgi.py')
    if not os.path.exists(new_wsgi_file_path):
        default_wsgi_file_path = os.path.join(base_dir, 'fao_case_list_wsgi.py.tpl')
        with open(default_wsgi_file_path) as default_wsgi_file:
            with open(new_wsgi_file_path, 'w') as new_wsgi_file:
                new_wsgi_file.write(default_wsgi_file.read())
        print('WSGI file {} successfully created.'.format(new_wsgi_file_path))


if __name__ == '__main__':
    create_settings()
    create_wsgi()
