web: gunicorn MoneySystem.wsgi --log-file -
init: python manage.py migrate
upgrade: python manage.py migrate