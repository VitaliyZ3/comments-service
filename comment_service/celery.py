import os
from celery import Celery

IS_PRODUCTION = os.environ.get('IS_PRODUCTION')
if IS_PRODUCTION:
    django_setting_path = 'comment_service.conf.production.settings'
else:
    django_setting_path = 'comment_service.conf.development.settings'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_setting_path)
app = Celery("comment_service", broker_connection_retry_on_startup=True)
app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()

