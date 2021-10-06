#!/bin/sh

set -e #dont continue commands if something fails

python manage.py collectstatic --noinput

## RUN GUNICORN
gunicorn plato.wsgi -b 0.0.0.0:8000

