#!/bin/bash
manage.py migrate core
manage.py migrate venues
manage.py migrate competitions
manage.py migrate teams
manage.py migrate opposition
manage.py migrate members
manage.py migrate matches
manage.py migrate awards
manage.py migrate training
manage.py migrate feedback
