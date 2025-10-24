echo "Starting server with $GUNICORN_WORKERS workers"
gunicorn -b 0.0.0.0:80 -w $GUNICORN_WORKERS --log-config app/settings/logging.config --capture-output --log-level info 'app.wsgi:application'