import os
from .base import *
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY environment variable is not set.")

DEBUG = False  # Should be False in production!

ALLOWED_HOSTS = ['127.0.0.1', '170.9.20.139', 'mambohealth.eu.org', 'www.mambohealth.eu.org']

try:
    from .local import *
except ImportError:
    pass
