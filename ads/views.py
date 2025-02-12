
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .forms import AdForm
from django.shortcuts import render


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


# Добавление объявления (доступно только авторизованным пользователям)
@login_required(login_url='/login/')
def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            # Проверка размера видео (например, максимальный размер 100MB)
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
    paginator = Paginator(ads_list, 10)  # Показывать 10 объявлений на странице
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
def ads_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ads_list.html', {'ads': ads})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')