#!-*- coding=utf-8 -*-

#vitualenv supports
import site
site.addsitedir('C:/Users/Administrator/Envs/touch_health/Lib/site-packages')

import os, sys
#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
root=os.path.dirname(workspace)

#output to error.log
sys.stdout = sys.stderr
#sys.path.append(root)
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ask_price.settings.prod_test'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()