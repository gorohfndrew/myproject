from django.contrib import admin
from django.urls import path, include
from ads.views import ads_list  # <-- Импортируем ads_list правильно

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ads_list, name='ads_list'),  # <-- Добавляем представление напрямую
    path('ads/', include('ads.urls')),  # <-- Подключаем маршруты приложения ads
]
