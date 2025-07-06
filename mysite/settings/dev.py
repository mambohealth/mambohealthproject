from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rkof=ig_pmabyz^&z^=$6rxx%pbp1!u53wl1fxs8u_s$!t!!%q"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"


try:
    from .local import *
except ImportError:
    pass
