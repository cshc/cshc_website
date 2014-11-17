#!/bin/bash
# Usage: revert_db.sh <dump.sql>
#
# where <dump.sql> is the mysqldump output file to restore the DB from.

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "You must specify the mysqldump file to use"

read -p "This will DROP ALL TABLES from the database and restore the backup. Are you sure you want to continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    MYSQL="mysql -h mysql-51.int.mythic-beasts.com -u cshc -pkilaekie -D cshc"
    echo Dropping all DB tables...
    $MYSQL -BNe "show tables" | awk '{print "set foreign_key_checks=0; drop table `" $1 "`;"}' | $MYSQL
    echo Restoring DB to backed up state...
    $MYSQL < $1
    echo Done!
    unset MYSQL
fi
