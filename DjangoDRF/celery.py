import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoDRF.settings')

app = Celery('DjangoDRF')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()