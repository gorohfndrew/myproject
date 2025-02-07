from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ads import AdViewSet, CategoryViewSet, ads_list, ad_detail, add_ad, site_rules, about, RegisterView
from django.conf import settings
from django.conf.urls.static import static

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
    path('api/v1/', include(router.urls)),  # Подключаем API с префиксом
    path('api-auth/', include('rest_framework.urls')),  # Авторизация в DRF
    path('register/', RegisterView.as_view(), name='register'),  # Страница регистрации
    path('about/', about, name='about'),  # Додайте цей шлях для сторінки "Про нас"
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)