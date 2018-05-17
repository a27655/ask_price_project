"""
WSGI config for ask_price_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import sys
import os
import site

site.addsitedir('/root/.vituralenvs/ask_price/lib/python2.7/site-packages')
# rom django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_price.settings.prod")

# Add the  project  directory
# sys.path.append('/home/nginxuser/nginxuser')
PROJECT_DIR = '/home/qian/ask_price/ask_price'
sys.path.insert(0, PROJECT_DIR)
# Activate your virtual env
activate_env = os.path.expanduser("/root/.virtualenvs/ask_price/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

# after activite env
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()