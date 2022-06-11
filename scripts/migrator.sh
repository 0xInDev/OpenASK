#!/bin/bash
python manage.py makemigrations
python manage.py makemigrations $1
python manage.py migrate

read -p "Create new user [Y/N]? " choice

choice="${choice:-N}"

if [ $choice = 'Y' ] || [ $choice = 'y' ]
then
    python manage.py createsuperuser
fi