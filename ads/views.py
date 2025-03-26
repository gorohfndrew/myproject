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

class AdsListView(ListView):
    model = Ad
    template_name = "ads/ads_list.html"  # Вкажіть правильний шлях до шаблону
    context_object_name = "ads"

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
            
            # 🛠 Обрабатываем изображение
            image_file = request.FILES.get('image')  
            if image_file:
                ad.image = image_file  # Сохраняем в Cloudinary
            
            # 🛠 Проверяем видео
            video_file = request.FILES.get('video')
            if video_file and video_file.size > 104857600:  # 100MB
                form.add_error('video', 'Максимальный размер видео 100MB.')
            else:
                ad.save()  # Теперь изображение точно сохранится!
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
            return redirect('ads_list')  # Перенаправлення на список оголошень
    else:
        form = RegistrationForm()

    return render(request, 'ads/register.html', {'form': form})

def home(request):
    return render(request, 'ads/home.html')