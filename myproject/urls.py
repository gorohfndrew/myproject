from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ads.views import AdViewSet, CategoryViewSet, ads_list, ad_detail, add_ad, site_rules, about, RegisterView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views  # Импортируем представления для логина и логаута

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
    path('about/', about, name='about'),  # Страница "Про нас"
    path('admin/', admin.site.urls),  # Страница администрирования
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Страница входа
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Страница выхода
]

# Для работы с медиа-файлами в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)