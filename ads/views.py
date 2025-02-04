from django.shortcuts import render
from django.urls import path  
from rest_framework import viewsets
from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer

 

# ✅ ПРАВИЛЬНО: Объявляем функцию ads_list
def ads_list(request):
    return render(request, 'ads/ads_list.html')  # Убедись, что шаблон существует

urlpatterns = [
    path('', ads_list, name='ads_list'),  # ✅ Теперь ads_list определён правильно
]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
