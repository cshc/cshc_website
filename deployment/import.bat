echo Importing data...
python manage.py data_migration
python manage.py create_users
python manage.py import_data --all
python manage.py import_league_tables