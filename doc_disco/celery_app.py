import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doc_disco.settings')

app = Celery('doc_disco')
app.config_from_object('doc_disco.settings.celery_config')

app.autodiscover_tasks()
