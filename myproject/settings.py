import os
from pathlib import Path
import environ
import dj_database_url
import logging
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Создаём экземпляр environ и загружаем переменные окружения
env = environ.Env()
env_file = BASE_DIR / '.env'  # Указываем путь к .env файлу
environ.Env.read_env(env_file)  # Загрузка переменных окружения из файла .env

# Читаем переменные с использованием environ
SECRET_KEY = env("SECRET_KEY", default=None)  
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables.")  
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"SECRET_KEY: {SECRET_KEY}")

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'django_celery_results',


    'rest_framework',
    'ads',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'
load_dotenv()
# Загружаем переменные из .env
DATABASE_URL = os.getenv('DATABASE_URL')

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

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Russian'),
    ('en', 'English'),
]

# Настройки статики
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Настройки медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
LOGIN_REDIRECT_URL = '/ads/'  
# Разрешенные файлы
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

env = environ.Env()
environ.Env.read_env()  # Чтение .env файла

# Настройки Celery из .env файла
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='sqla+postgresql://username:password@localhost/dbname')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='django-db')
CELERY_ACCEPT_CONTENT = env.list('CELERY_ACCEPT_CONTENT', default='json')
CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER', default='json')

# Поддержка загрузки больших файлов
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