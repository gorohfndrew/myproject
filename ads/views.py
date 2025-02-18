from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rest_framework import viewsets

from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .forms import AdForm
from django.http import JsonResponse
from .models import User
from django.contrib.auth.forms import UserCreationForm


# Регистрация пользователей
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "ads/register.html"
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        next_url = self.request.GET.get('next', self.success_url)
        return redirect(next_url)


# API для объявлений
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


# API для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Добавление объявления (только для авторизованных пользователей)
@login_required(login_url='/login/')
def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            video_file = request.FILES.get('video')
            if video_file and video_file.size > 104857600:  # 100MB
                form.add_error('video', 'Максимальный размер видео 100MB.')
            else:
                ad.save()
                return redirect('ads_list')
    else:
        form = AdForm()
    return render(request, 'ads/add_ad.html', {'form': form})


# Список объявлений с пагинацией
def ads_list(request):
    ads_list = Ad.objects.all()
    paginator = Paginator(ads_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ads/ads_list.html', {'page_obj': page_obj})


# Детали объявления
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


# Правила сайта
def site_rules(request):
    return render(request, 'ads/rules.html')


# Страница "О нас"
def about(request):
    return render(request, 'ads/about.html')


# Политика конфиденциальности
def privacy_policy(request):
    return render(request, 'ads/privacy_policy.html')


# Фильтрация объявлений по категориям
def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    ads = Ad.objects.filter(category=category)
    return render(request, 'ads/category_ads.html', {'category': category, 'ads': ads})

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'ads/categories.html', {'categories': categories})




# Поиск объявлений
def search_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    results = Ad.objects.all().order_by('-created_at')  # Сортируем по дате

    if query:
        results = results.filter(title__icontains=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        results = results.filter(category=category)

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'ads/search_results.html', {
        'page_obj': page_obj,
        'query': query,
        'category_slug': category_slug,
        'categories': categories
    })

def advertisements_view(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        ads = Ad.objects.filter(category=category)
    else:
        ads = Ad.objects.all()
    return render(request, 'ads/advertisements_list.html', {'ads': ads})
