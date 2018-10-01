#!bin/bash

set -e
cd /src

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn budgets.wsgi:application -w 3 -b :8000
# python manage.py runserver 0.0.0.0:8000
