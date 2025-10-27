echo "Starting server with $DJANGO_GUNICORN_WORKERS workers"
gunicorn -b 0.0.0.0:80 -w $DJANGO_GUNICORN_WORKERS --capture-output --log-level info 'app.wsgi:application'