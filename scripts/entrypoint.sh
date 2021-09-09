#!/bin/sh

set -e #dont continue commands if something fails

python manage.py collectstatic --noinput

gunicorn --env DJANGO_SETTINGS_MODULE=test-settings plato.wsgi -b 127.0.0.1:8000

