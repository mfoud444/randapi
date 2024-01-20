#!/bin/bash
cd randai
#pip install -U g4f
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
#python manage.py runserver 10.2.99.12:8000
