from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .templates.ads.views import AdViewSet, CategoryViewSet, ads_list, ad_detail, add_ad, site_rules

# Создаём роутер и регистрируем ViewSet'ы
router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'categories', CategoryViewSet)

# Определяем маршруты
urlpatterns = [
    path('', ads_list, name='ads_list'),  # Главная страница объявлений
    path('rules/', site_rules, name='site_rules'),  # Страница правил
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),  # Страница одного объявления
    path('add/', add_ad, name='add_ad'),  # Форма добавления объявления
    path('api/', include(router.urls)),  # Подключаем API
]