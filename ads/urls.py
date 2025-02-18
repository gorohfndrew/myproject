from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views
from ads.views import AdViewSet, CategoryViewSet, ad_detail, add_ad, site_rules, about, privacy_policy, RegisterView, AdsListView

# Создаём роутер и регистрируем ViewSet'ы
router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('ads/', views.ads_list, name='ads_list'),  # Список объявлений
    path('rules/', site_rules, name='site_rules'),  # Страница правил
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),  # Страница одного объявления
    path('add/', add_ad, name='add_ad'),  # Форма добавления объявления
    path('register/', RegisterView.as_view(), name='register'),  # Страница регистрации
    path('about/', about, name='about'),  # Страница "Про нас"
    path('privacy-policy/', privacy_policy, name='privacy_policy'),  # Страница политики конфиденциальности
    path('categories/', views.categories_view, name='categories'),  # Страница категорий
    path('search_results/', views.search_view, name='search_results'),  # Результаты поиска
    path('advertisements/category/<slug:category_slug>/', views.category_view, name='category_ads'),  # Фильтрация по категориям
    path("", AdsListView.as_view(), name="home"),  # Главная страница с использованием AdsListView

    # Подключение API
    path('api/v1/', include(router.urls)),  # Подключаем API с префиксом
    path('api-auth/', include('rest_framework.urls')),  # Авторизация в DRF
]

# Для работы с медиа-файлами в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    