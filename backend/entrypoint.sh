#!/bin/sh
python manage.py migrate --no-input
python manage.py collectstatic --no-input

uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --log-level info
