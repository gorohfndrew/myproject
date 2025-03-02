from django.urls import path
from . import views

app_name = 'ads'  # Простір імен для додатка ads

urlpatterns = [
    path('', views.ads_list, name='ads_list'),  # Список всіх оголошень
    path('categories/', views.categories_list, name='categories'),  # Сторінка категорій
    path('category/<slug:category_slug>/', views.ads_list, name='category_ads'),  # Фільтр по категорії
    path('rules/', views.site_rules, name='site_rules'),  # Сторінка правил
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('add/', views.add_ad, name='add_ad'),  # Додавання оголошення
    path('register/', views.RegisterView.as_view(), name='register'),  # Реєстрація
    path('about/', views.about, name='about'),  # Про нас
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Політика конфіденційності
    path('search_results/', views.search_view, name='search_results'),  # Пошук
]