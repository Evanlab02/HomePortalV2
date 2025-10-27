celery -A app worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
