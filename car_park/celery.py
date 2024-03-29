import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# указываем место нажождения настройек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_park.settings")

app = Celery('car_park')

# указываем celery искать настройки в файле settings
# которые начинаются с CELERY
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object(settings, namespace='CELERY')
# Указываем авмтоматически подцеплять такси
app.autodiscover_tasks()


app.conf.beat_schedule = {
	'check-last-inspection': {
		'task': "cabinet.tasks.check_last_inspection",
		'schedule': crontab(minute='*/60'),
	},
	'delete-empty-card': {
		'task': "cabinet.tasks.delete_empty_card",
		'schedule': crontab(minute='*/60'),
	},
	'check-car-docs-date': {
		'task': "cabinet.tasks.check_car_docs_date",
		'schedule': crontab(minute='*/60'),
	},
	'check_user_docs_date': {
		'task': "cabinet.tasks.check_user_docs_date",
		'schedule': crontab(minute='*/60'),
	},
	'create-note-about-ending-cards': {
		'task': "cabinet.tasks.create_note_about_ending_cards",
		'schedule': crontab(minute='*/60'),
	},

}