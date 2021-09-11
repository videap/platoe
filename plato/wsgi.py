"""
<<<<<<< HEAD
WSGI config for Plato project.
=======
WSGI config for plato project.
>>>>>>> docker

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plato.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev-settings')
>>>>>>> docker

application = get_wsgi_application()
