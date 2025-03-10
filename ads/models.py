from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import admin

User = get_user_model()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Отображаем пользователя и телефон
    search_fields = ('user__username', 'phone_number')  # Добавляем поиск

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

# Категория объявления
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    icon = models.CharField(max_length=100, default="default-icon.png")
    description = models.TextField()
    ad_count = models.PositiveIntegerField(default=0)  # Поле для подсчета объявлений

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update_ad_count(self):
        # Подсчитываем количество объявлений в категории
        self.ad_count = self.ads.count()
        self.save()

    def __str__(self):
        return self.name
# Объявление
class Ad(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='ads')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец объявления

    title = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='ads_videos/', null=True, blank=True)

    # Статусы объявления
    is_boosted = models.BooleanField(default=False)
    is_standard = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)

    @property
    def is_premium_active(self):
        """Проверяет, активен ли статус премиум."""
        return bool(self.premium_until and self.premium_until > timezone.now())

    def __str__(self):
        return self.title


# Админка для объявлений
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_tag', 'video_tag', 'is_premium', 'is_premium_active', 'premium_until')
    list_filter = ('is_premium', 'is_boosted', 'is_standard', 'is_popular')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" />')
        return '-'
    
    image_tag.short_description = "Изображение"

    def video_tag(self, obj):
        if obj.video:
            return mark_safe(f'<video width="100" controls><source src="{obj.video.url}" type="video/mp4">Ваш браузер не поддерживает видео.</video>')
        return 'Нет видео'
    
    video_tag.short_description = "Видео"

    def is_premium_active(self, obj):
        return obj.is_premium_active  # Теперь это свойство модели
    is_premium_active.boolean = True
    is_premium_active.short_description = 'Премиум активен'
