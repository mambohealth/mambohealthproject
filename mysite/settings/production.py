from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '170.9.20.139', 'mambohealth.eu.org', 'www.mambohealth.eu.org']

try:
    from .local import *
except ImportError:
    pass
