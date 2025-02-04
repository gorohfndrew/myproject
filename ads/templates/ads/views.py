from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path  # 
from rest_framework import viewsets
from .models import Ad, Category
from ...serializers import AdSerializer, CategorySerializer
from .forms import AdForm  

# ✅ ПРАВИЛЬНО: Объявляем функцию ads_list
def ads_list(request):
    return render(request, 'ads/ads_list.html')  # Убедись, что шаблон существует
def site_rules(request):
    return render(request, 'ads/rules.html')
def ads_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ads_list.html', {'ads': ads})

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ads_list')
    else:
        form = AdForm()
    return render(request, 'ads/add_ad.html', {'form': form})

urlpatterns = [
    path('', ads_list, name='ads_list'),  # ✅ Теперь ads_list определён правильно
]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer