import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/fuglaeff/innopolis_job'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
