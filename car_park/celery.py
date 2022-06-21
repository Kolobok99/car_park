import os
from celery import Celery
from celery.schedules import crontab

# указываем место нажождения настройек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")

app = Celery('car_park')

# указываем celery искать настройки в файле settings
# которые начинаются с CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Указываем авмтоматически подцеплять такси
app.autodiscover_tasks()


app.conf.beat_schedule = {
	'check-last-inspection-every-1-minute': {
		'task': "cabinet.tasks.check_last_inspection",
		'schedule': crontab(minute='*/1'),
	},
	'delete-empty-card': {
		'task': "cabinet.tasks.delete_empty_card",
		'schedule': crontab(minute='*/1'),
	},
}