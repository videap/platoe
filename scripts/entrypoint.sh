#!/bin/sh

set -e #dont continue commands if something fails

python manage.py collectstatic --noinput

gunicorn --env DJANGO_SETTINGS_MODULE=test-settings plato.wsgi -b 0.0.0.0:8000

