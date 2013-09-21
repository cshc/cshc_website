echo Migrating models
python manage.py migrate core --fake
python manage.py migrate venues --fake
python manage.py migrate competitions --fake
python manage.py migrate teams --fake
python manage.py migrate opposition --fake
python manage.py migrate members --fake
python manage.py migrate matches --fake
python manage.py migrate awards --fake
python manage.py migrate training --fake
python manage.py migrate feedback --fake
