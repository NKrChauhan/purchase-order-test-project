#!/bin/bash

# Apply Django database migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test

# Run server
python manage.py runserver 0.0.0.0:8000
