#!/bin/bash

# Execute startup scripts
./wait-for-postgres.sh "$DBHOST"
python3 /app/manage.py collectstatic --noinput
python3 /app/manage.py migrate
python3 /app/manage.py runserver 0.0.0.0:8000