#!/bin/sh
echo '{"loglevel":"info", "message":"App starting"}'
nc -z localhost 5432
python manage.py migrate
python manage.py runserver 0.0.0.0:${PORT}