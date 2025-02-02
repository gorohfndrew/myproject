"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

# Импортируем приложение Flask
from mydona.app import app  # Замените 'app' на имя вашего файла Flask-приложения

# Назначаем переменную application для использования в Gunicorn
application = app

# Если у вас есть Django настройки, то используйте их как ранее
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Для Django приложения также указываем вызов get_wsgi_application (это для Django)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()