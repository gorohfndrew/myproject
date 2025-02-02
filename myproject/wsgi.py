"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from mydona.app import app  # Flask-приложение

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Создаем WSGI приложение для Django
django_application = get_wsgi_application()

# Совмещаем Django и Flask приложения (это необычно и сложнее)
application = app  # Для Flask-приложения можно использовать Flask, если это необходимо