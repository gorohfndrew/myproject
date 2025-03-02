from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ads import views
# API Router
router = DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include(('ads.urls', 'ads'), namespace='ads')),  # Подключаем ads.urls с пространством имен
    path('', views.ads_list, name='ads_list'),  # Главная страница
    path('api/v1/', include(router.urls)),  # Подключаем API
    path('api-auth/', include('rest_framework.urls')),  # DRF авторизация
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
]

# Поддержка медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
