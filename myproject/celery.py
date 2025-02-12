from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import worker_ready

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Настройка PostgreSQL как брокер
app.conf.update(
    broker_url='postgresql://your_user:your_password@localhost/your_db',
    result_backend='postgresql://your_user:your_password@localhost/your_db',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.update(
    CELERY_RESULT_BACKEND=f'postgresql://{os.getenv("DATABASE_URL")}'
)

# Подключение к Django
@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    print("Celery worker is ready!")