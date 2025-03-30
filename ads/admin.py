from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Profile, Category, Ad
from django.contrib.admin import TabularInline
from .models import Ad, AdImage




class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Показывает поля в списке
    search_fields = ('user__username', 'phone_number')  # Добавляет поиск по полям
    fields = ('user', 'phone_number')  # Указывает, какие поля отображать на странице редактирования


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Дополнительная информация"
    fields = ('phone_number',)  # Поле для редактирования номера телефона


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'get_phone_number', 'is_staff')

    def get_phone_number(self, obj):
        if hasattr(obj, 'profile') and obj.profile.phone_number:
            return obj.profile.phone_number
        return "Нет номера"
    get_phone_number.short_description = "Номер телефона"


# Админка для работы с категориями
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение поля slug по полю name


# Админка для работы с объявлениями
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_tag', 'video_tag', 'is_premium', 'is_premium_active', 'premium_until')
    list_filter = ('is_premium', 'is_boosted', 'is_standard', 'is_popular')
    search_fields = ('title', 'description')  
    ordering = ('-created_at',)

    # Измененный метод для отображения изображения из связанной модели AdImage
    def image_tag(self, obj):
        # Получаем изображение из связанной модели AdImage
        ad_image = obj.images.first()  # Возвращает первое изображение для объявления (или None, если нет изображений)
        if ad_image and ad_image.image:
            return mark_safe(f'<img src="{ad_image.image.url}" width="100px" />')
        return '-'
    image_tag.short_description = "Изображение"

    # Для отображения видео - оставляем так, как есть, если видео есть в модели Ad
    def video_tag(self, obj):
        """Отображает видео в админке."""
        if obj.video:
            return mark_safe(f'<video width="100" controls><source src="{obj.video.url}" type="video/mp4">Ваш браузер не поддерживает видео.</video>')  
        return 'Нет видео'
    video_tag.short_description = "Видео"

    # Статус активности премиума
    def is_premium_active(self, obj):
        """Проверка, активен ли статус премиум."""
        return obj.is_premium_active
    is_premium_active.short_description = 'Премиум активен'

# Удаляем стандартную регистрацию User, чтобы использовать CustomUserAdmin


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)