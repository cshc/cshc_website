echo Migrating models
manage.py migrate core --fake
manage.py migrate venues --fake
manage.py migrate competitions --fake
manage.py migrate teams --fake
manage.py migrate opposition --fake
manage.py migrate members --fake
manage.py migrate matches --fake
manage.py migrate awards --fake
manage.py migrate training --fake
manage.py migrate feedback --fake
