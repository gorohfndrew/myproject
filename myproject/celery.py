from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import worker_ready

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Чтение значений из переменных окружения
broker_url = os.getenv('CELERY_BROKER_URL')
result_backend = os.getenv('CELERY_RESULT_BACKEND')

# Настройка PostgreSQL как брокер и для хранения результатов
app.conf.update(
    broker_url=broker_url,
    result_backend=result_backend,
)

# Настройка Celery с использованием параметров из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

# Сигнал для оповещения, когда worker готов
@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    print("Celery worker is ready!")