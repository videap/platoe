"""
<<<<<<< HEAD
ASGI config for Plato project.
=======
ASGI config for plato project.
>>>>>>> docker

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plato.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev-settings')
>>>>>>> docker

application = get_asgi_application()
