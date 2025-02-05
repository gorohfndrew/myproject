from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path, include  # include нужно для подключения REST API
from rest_framework import viewsets
from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .forms import AdForm  # Импортируем форму AdForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  # Импортируем login
from django.contrib.auth.decorators import login_required
from django.views import View

class RegisterView(View):
    def get(self, request):
        return render(request, 'ads/register.html')  # Укажите правильный путь

# Представление для регистрации
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"  # Убедитесь, что этот шаблон существует
    success_url = "/"  # После успешной регистрации перенаправит на главную (ads_list.html)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Автоматический вход после регистрации
        return response

# Функция для добавления нового объявления
@login_required
def add_ad(request):
    """Создание нового объявления"""
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user  # Присваиваем пользователя
            ad.save()
            return redirect('ads_list')  # Перенаправляем на список объявлений
    else:
        form = AdForm()

    return render(request, 'ads/add_ad.html', {'form': form})

# Функция для отображения списка объявлений
def ads_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ads_list.html', {'ads': ads})

# Функция для отображения правил
def site_rules(request):
    return render(request, 'ads/rules.html')

# Функция для отображения подробной информации об одном объявлении
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

# URL-маршруты
urlpatterns = [
    path('', ads_list, name='ads_list'),  # Главная страница объявлений
    path('rules/', site_rules, name='site_rules'),  # Страница правил
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),  # Страница одного объявления
    path('add/', add_ad, name='add_ad'),  # Форма добавления объявления
    path('register/', RegisterView.as_view(), name='register.'),  # Страница регистрации

]

# ViewSet для Category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSet для Ad
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer