from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ads import views
from ads.views import home
from ads.views import register
from ads.views import custom_login
from django.contrib.auth.views import LogoutView
from ads.views import login_redirect


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
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', login_redirect, name='login'),     
                  
]
    


# Поддержка медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
