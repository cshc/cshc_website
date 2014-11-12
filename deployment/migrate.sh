#!/bin/bash
python manage.py migrate core
python manage.py migrate venues
python manage.py migrate competitions
python manage.py migrate teams
python manage.py migrate opposition
python manage.py migrate members
python manage.py migrate matches
python manage.py migrate awards
python manage.py migrate training
