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
        'schedule': crontab(hour=8, minute=18)
    },
    # 'blockio_transfer_usd_to_user_balance-each-5-minutes': {
    #     'task': 'finance.blockio_transfer_usd_to_user_balance_task',
    #     'schedule': crontab(minute='*/1')
    # },
    # 'points-awars-each-thursday-in-6h-10m': {
    #     'task': 'award.start_point_awadr_task',
    #     'schedule': crontab(hour=6, minute=10, day_of_week=2)
    # },
}
