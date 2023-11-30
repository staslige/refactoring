import os
from django.core.wsgi import get_wsgi_application
import importlib
module_name = 'profisrael'
special_module = importlib.import_module(module_name, package=None)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profisrael.settings')

application = get_wsgi_application()