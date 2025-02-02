from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут для админки
    path('', include('ads.urls')),  # Подключение маршрутов приложения ads
]

# Добавляем маршруты для статических и медиа-файлов (например, для изображений в объявлениях)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)