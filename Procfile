web: gunicorn run:app --preload
release: python manage.py db init
release: python manage.py db migrate
release: python manage.py db upgrade
 
