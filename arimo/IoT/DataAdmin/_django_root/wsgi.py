import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arimo.IoT.DataAdmin._project.settings')
application = get_wsgi_application()
