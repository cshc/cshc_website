echo Importing data...
manage.py data_migration
manage.py create_users
manage.py import_data --all
manage.py import_league_tables