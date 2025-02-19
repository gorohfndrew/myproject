from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ads import views

# Создаём роутер и регистрируем ViewSet'ы
router = DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'categories', views.CategoryViewSet)

# Определяем маршруты
urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.ads_list, name='ads_list'),  
    path('ads/', views.ads_list, name='ads_list'),  
    path('rules/', views.site_rules, name='site_rules'),  
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),  
    path('add/', views.add_ad, name='add_ad'),  
    path('register/', views.RegisterView.as_view(), name='register'),  
    path('about/', views.about, name='about'),  
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),    
    path('search_results/', views.search_view, name='search_results'),
    path('categories/', views.categories_list, name='categories_list'), 
    path("register/", views.register, name="register"),
    
    # Путь для фильтрации объявлений по категориям
    path('advertisements/category/<slug:category_slug>/', views.category_view, name='category_ads'),

    # Подключаем API
    path('api/v1/', include(router.urls)),  
    path('api-auth/', include('rest_framework.urls')),  
]

# Для работы с медиа-файлами в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)