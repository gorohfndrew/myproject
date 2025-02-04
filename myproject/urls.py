from django.contrib import admin
from django.urls import path, include
from ads.templates.ads.views import ads_list  # <-- Импортируем ads_list правильно
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', ads_list, name='ads_list'),
    path('ads/', include('ads.urls')),
]


