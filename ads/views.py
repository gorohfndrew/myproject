from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rest_framework import viewsets
from .forms import RegistrationForm
from ads import views
from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .forms import AdForm
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .forms import CustomUserForm
from .models import Ad, AdImage
from django.contrib import messages
from django.views.generic import DetailView
import logging
from django.http import HttpResponseRedirect  # Добавьте этот импорт в начало файла
from django.urls import reverse

User = get_user_model()  # ✅ Определяем модель пользователя

def user_list():
    users = User.objects.all()  # Теперь можно работать с пользователями
    return users
class UserListView(ListView):
    model = CustomUser
    template_name = "ads/user_list.html"
    context_object_name = "users"
    paginate_by = 10


# Регистрация пользователейclass RegisterView(CreateView):
class RegisterView(CreateView):
    form_class = RegistrationForm  # Используем вашу форму регистрации
    template_name = "ads/register.html"
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        user = form.save()  # Сохраняем пользователя
        login(self.request, user)  # Логиним пользователя после успешной регистрации
        next_url = self.request.GET.get('next', self.success_url)  # Если есть next, то редирект туда
        return redirect(next_url)    
# API для объявлений
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def retrieve(self, request, *args, **kwargs):
        """ Увеличивает количество просмотров при каждом просмотре объявления. """
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)

class AdsListView(ListView):
    model = Ad
    template_name = "ads/ads_list.html"  # Вкажіть правильний шлях до шаблону
    context_object_name = "ads"

    def get_queryset(self):
        """ Просто получаем все объявления без увеличения просмотров. """
        return Ad.objects.all()

class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"  # Проверь правильность пути к шаблону

    def get_object(self, queryset=None):       
        """ Увеличивает количество просмотров при открытии объявления. """
        ad = super().get_object(queryset)
        
        ad.views_count += 1
        ad.save(update_fields=['views_count'])
        return ad    

# API для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@login_required(login_url='/login/')
def add_ad(request):
    if request.method == 'POST':
        print(f"Данные запроса: {request.POST}")  
        print(f"Файлы запроса: {request.FILES}")  

        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()

            # Получаем файлы правильно!
            images = request.FILES.getlist('images')  # ✅ Вместо `cleaned_data.get`
            print(f"Файлы получены: {images}")  

            for image in images:
                # ✅ Проверяем, является ли файл видео
                if hasattr(image, 'content_type') and image.content_type.startswith('video/'):
                    messages.error(request, "На даному етапі публікація відео не дозволена!")
                    return render(request, 'ads/add_ad.html', {'form': form})

                print(f"Сохраняем изображение: {image}")  
                AdImage.objects.create(ad=ad, image=image)  # ✅ Без `.file`

            # Проверяем видео
            video_file = request.FILES.get('video')
            if video_file and video_file.size > 104857600:  
                form.add_error('video', 'Максимальный размер видео 100MB.')
            else:
                return redirect('ads_list')
    else:
        form = AdForm()

    return render(request, 'ads/add_ad.html', {'form': form})
# Список объявлений с пагинацией
def ads_list(request, category_slug=None):
    # Получаем категорию, если передан slug
    category = None
    if category_slug:
        category = Category.objects.filter(slug=category_slug).first() # Используем .first(), чтобы избежать ошибки, если категория не найдена
        ads = Ad.objects.filter(category=category)
    else:
        ads = Ad.objects.all()

    # Пагинация
    paginator = Paginator(ads, 10)  # По 10 объявлений на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET параметра
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ads_list.html', {'category': category, 'page_obj': page_obj})

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    ad.views_count += 1
    ad.save(update_fields=['views_count'])
    return render(request, 'ads/ad_detail.html', {'ad': ad})


# Правила сайта
def site_rules(request):
    return render(request, 'ads/rules.html', {})

# Страница "О нас"
def about(request):
    return render(request, 'ads/about.html')


# Политика конфиденциальности
def privacy_policy(request):
    return render(request, 'ads/privacy_policy.html')


# Фильтрация объявлений по категориям
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    first_ad = Ad.objects.filter(category=category).first()

    if first_ad:
        return redirect('ad_detail', first_ad.id)  # Перенаправляем на первое объявление

    return render(request, 'ads/category_detail.html', {'category': category})
def categories_list(request):
    # Получаем все категории
    categories = Category.objects.all()

    # Создаём словарь для хранения количества объявлений в каждой категории
    category_ads = {}

    # Проходим по всем категориям и получаем количество объявлений в каждой категории
    for category in categories:
        ads_count = Ad.objects.filter(category=category).count()
        category_ads[category.slug] = ads_count  # Используем slug в качестве ключа
        print(f"Категория: {category.name}, Слаг: {category.slug}")

    # Отображаем шаблон с категориями и количеством объявлений
    return render(request, 'ads/categories.html', {
        'categories': categories,
        'category_ads': category_ads
    })
    

def category_view(request, category_slug):
    # Получаем категорию по slug, если нет - возвращаем 404
    category = get_object_or_404(Category, slug=category_slug)
    
    # Получаем все объявления для этой категории (без пагинации)
    ads = Ad.objects.filter(category=category).order_by('-created_at')  # сортируем по дате создания, можно изменить порядок

    # Передаем данные в шаблон
    return render(
        request,
        'ads/categories.html',
        {'category': category, 'ads': ads}
    )


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

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Створення нового користувача
            login(request, user)  # Авторизація користувача після реєстрації
            response = HttpResponseRedirect(reverse('ads_list'))  # 1. Создаем response
            response.set_cookie('user_id', user.id, max_age=157680000)  # 2. Устанавливаем cookie
            return response  # 3. Возвращаем response
    else:
        form = RegistrationForm()

    return render(request, 'ads/register.html', {'form': form})

def home(request):
    # Если пользователь авторизован - перенаправляем на ads_list
    if request.user.is_authenticated:
        return redirect('ads_list')
    return render(request, 'ads/home.html')

def contact(request):
    return render(request, "ads/contact.html")

def custom_login(request):
    return render(request, 'login.html', {'message': "Спочатку зареєструйтесь!"})
def auto_login(request):
    if request.user.is_authenticated:
        return redirect('ads_list')
    
    # Проверяем cookies
    user_id = request.COOKIES.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            login(request, user)
            return redirect('ads_list')
        except User.DoesNotExist:
            pass
    
    return redirect('register')  # Если нет cookies - на регистрацию