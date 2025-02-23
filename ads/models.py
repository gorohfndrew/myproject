from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()

# Категория объявления
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    icon = models.CharField(max_length=100, default="default-icon.png")
    description = models.TextField()  # Описание категории

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.name)  # Автоматически создаем slug из name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Объявление
class Ad(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='ads')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец объявления

    title = models.CharField(max_length=255)
    description = models.TextField()  # Описание объявления
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)  # Для изображений
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='ads_videos/', null=True, blank=True)  # Добавляем поле для видео

    # Дополнительные поля для статусов
    is_boosted = models.BooleanField(default=False)
    is_standard = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)  # Премиум-объявления
    premium_until = models.DateTimeField(null=True, blank=True)  # Срок действия премиума

    def __str__(self):
        return self.title


# Админка для работы с объявлениями
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_tag', 'video_tag', 'is_premium', 'is_premium_active', 'premium_until')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" />')
        return '-'
    
    image_tag.short_description = "Изображение"

    def video_tag(self, obj):
        """Метод для отображения видео в админке."""
        if obj.video:
            return mark_safe(f'<video width="100" controls><source src="{obj.video.url}" type="video/mp4">Ваш браузер не поддерживает видео.</video>')
        return 'Нет видео'
    
    video_tag.short_description = "Видео"

    # Фильтрация по премиум-объявлениям в админке
    list_filter = ('is_premium', 'is_boosted', 'is_standard', 'is_popular')

    def is_premium_active(self, obj):
        """Проверка, активен ли статус премиум."""
        return bool(obj.premium_until and obj.premium_until > timezone.now())
    is_premium_active.short_description = 'Премиум активен'


