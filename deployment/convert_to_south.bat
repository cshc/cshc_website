echo Migrating models
python manage.py convert_to_south core
python manage.py convert_to_south venues
python manage.py convert_to_south competitions
python manage.py convert_to_south teams
python manage.py convert_to_south opposition
python manage.py convert_to_south members
python manage.py convert_to_south matches
python manage.py convert_to_south awards
python manage.py convert_to_south training
