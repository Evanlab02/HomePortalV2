echo "Running migrations..."
python manage.py migrate

echo "Starting admin server..."
gunicorn -b 0.0.0.0:80 -w 1 --capture-output --log-level info 'app.wsgi:application'