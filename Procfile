web: bash -lc "python manage.py collectstatic --noinput && gunicorn lifepath.wsgi --bind 0.0.0.0:$PORT --log-file -"

