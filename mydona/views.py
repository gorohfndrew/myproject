from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Ad, Category
from ads.views import categories_html

from .models import Ad


# Добавление объявления (доступно только авторизованным пользователям)


# Список объявлений с пагинацией
def ads_list(request):
    ads_list = Ad.objects.all()
    paginator = Paginator(ads_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ads/ads_list.html', {'page_obj': page_obj})



# Правила сайта
def site_rules(request):
    return render(request, 'ads/rules.html')


# Детали объявления
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

def about(request):
    return render(request, 'about.html')  # Переконайтеся, що у вас є шаблон about.html


def privacy_policy(request):
    return render(request, 'privacy_policy.html')



def advertisements_view(request):
    category_slug = request.GET.get('category')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        ads = Ad.objects.filter(category=category)
    else:
        ads = Ad.objects.all()

    return render(request, 'ads/ads_list.html', {'ads': ads, 'category_slug': category_slug})
def categories_html(request):
    categories = Category.objects.all()
    return render(request, 'categories_html.html', {'categories': categories})




def get_category_counts():
    categories = Category.objects.all()
    counts = {category.name: category.ads.count() for category in categories}
    return counts  # Теперь функция что-то возвращает

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    ads = Ad.objects.filter(category=category)
    return render(request, 'ads/category_ads.html', {'category': category, 'ads': ads})

def categories_view(request):
    categories = Category.objects.all()
    category_counts = {category.name: category.ads.count() for category in categories}  
    return render(request, 'categories.html', {
        'categories': categories,
        'category_counts': category_counts
    })

def search_results(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    results = Ad.objects.all()

    if query:
        results = results.filter(title__icontains=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        results = results.filter(category=category)

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/search_results.html', {
        'page_obj': page_obj,
        'query': query,
        'category_slug': category_slug
    })