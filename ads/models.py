from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils import timezone

User = get_user_model()

# Категория объявления
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Объявление
class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец объявления
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)  # Для изображений
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="videos/", blank=True, null=True)  # Поле для видео
    is_premium = models.BooleanField(default=False)  # Добавляем поле для премиум-объявлений
    premium_until = models.DateTimeField(null=True, blank=True)  # Срок действия премиума

    def __str__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/no-image.jpg"  # Путь к изображению по умолчанию

    def is_premium_active(self):
        """Проверка, активен ли статус премиум."""
        if self.premium_until and self.premium_until > timezone.now():
            return True
        return False


# Настройка отображения изображений в админке
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_url', 'is_premium', 'is_premium_active', 'premium_until')

    def image_url(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" />')
        return '-'

    image_url.allow_tags = True

    # Фильтрация по премиум-объявлениям в админке
    list_filter = ('is_premium',)


