echo Creating initial schema migrations
manage.py schemamigration core --initial
manage.py schemamigration venues --initial
manage.py schemamigration competitions --initial
manage.py schemamigration teams --initial
manage.py schemamigration opposition --initial
manage.py schemamigration members --initial
manage.py schemamigration matches --initial
manage.py schemamigration awards --initial
manage.py schemamigration training --initial
manage.py schemamigration feedback --initial
