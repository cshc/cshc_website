#!/bin/sh

export DATABASE_URL=sqlite:///`pwd`/db.sqlite

if [ $# -eq 2 ]
then
    DJANGO_COMMAND="$1 $2"
elif [ $# -ne 1 ]
then
    DJANGO_COMMAND=runserver
else
    DJANGO_COMMAND=$1
fi

python manage.py $DJANGO_COMMAND

