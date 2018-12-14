import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ppf.settings')

app = Celery('django_ppf')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update_horoz_task_every_day': {
        'task': 'assistant.update_horoz_task',
        'schedule': crontab(hour=16, minute=48)
    },
}
