import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
import environ
import dj_database_url
import logging
from pathlib import Path
from celery.schedules import crontab


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

if os.path.exists(env_file):
    env.read_env()  # Завантажуємо .env, якщо він є

# Завантажуємо SECRET_KEY
SECRET_KEY = env("SECRET_KEY", default="your-default-secret-key")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables.") 
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"SECRET_KEY: {SECRET_KEY}")

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
INSTALLED_APPS = [
    'ads',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'django_extensions',
    'rest_framework',
    'phonenumber_field',
    'cloudinary',
    'cloudinary_storage',
     
     
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',  # Додаємо сюди
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", BASE_DIR / "ads/templates", BASE_DIR / "ads/templates/ads"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myproject.context_processors.categories', 
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Настройки базы данных
DATABASE_URL = env('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    ),
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Russian'),
    ('en', 'English'),
    ('uk', 'Українська'),
]
SESSION_COOKIE_AGE = 157680000  # 5 лет в секундах (60*60*24*365*5)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Не очищать при закрытии браузера
SESSION_SAVE_EVERY_REQUEST = True  # Обновлять срок при активности

# Безопасность (обязательно для production)
SESSION_COOKIE_SECURE = True  # Только HTTPS
SESSION_COOKIE_HTTPONLY = True  # Защита от XSS
CSRF_COOKIE_SECURE = True  # Для CSRF-токенов
CSRF_COOKIE_AGE = SESSION_COOKIE_AGE  # Синхронизация сроков

# Дополнительно (рекомендуется)
SESSION_COOKIE_SAMESITE = 'Lax'  # Защита от CSRF
CSRF_COOKIE_SAMESITE = 'Lax'

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # для Render


# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
LOGIN_REDIRECT_URL = '/ads/'

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# Настройки Celery из .env файла
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='sqla+postgresql://username:password@localhost/dbname')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='django-db')
CELERY_ACCEPT_CONTENT = env.list('CELERY_ACCEPT_CONTENT', default=['json'])
CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER', default='json')

CELERY_BEAT_SCHEDULE = {
    'remove-expired-ads': {
        'task': 'ads.tasks.remove_expired_ads',
        'schedule': crontab(minute=0, hour=0),  # Запуск каждый день в полночь
    },
}

# Максимальный размер загружаемых файлов
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB

# Настройки DRF
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level':  "ERROR",
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': "ERROR",
            'propagate': True,
        },
    },
}

# Настройка пользовательской модели
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/"
AUTH_USER_MODEL = 'ads.CustomUser'
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # Ограничение на 10MB для всех файлов
LOGOUT_REDIRECT_URL = 'login'
