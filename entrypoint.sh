#!/bin/bash

sleep 10
python manage.py migrate
exec gunicorn wsgi:application --bind 0.0.0.0:8001

exec "$@"
