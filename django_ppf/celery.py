import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ppf.settings')

app = Celery('django_ppf')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # 'update_horoz_task_every_day': {
    #     'task': 'assistant.tasks.update_horoz_task',
    #     'schedule': crontab(hour=7, minute=30)
    # },
    'run_xml_spider_every_hour': {
        'task': 'assistant.tasks.run_xml_spider',
        'schedule': crontab(hour='*/1', minute=0)
    },
    'make_xml_for_rozetka_every_20_minutes': {
        'task': 'assistant.tasks.make_xml_for_rozetka',
        'schedule': crontab(minute='*/30'),
    },
    'make_xlsx_for_prom_every_20_minutes': {
        'task': 'assistant.tasks.make_xlsx_for_prom_task',
        'schedule': crontab(minute='*/20'),
    }
}
