from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Ad, Category


# Админка для работы с категориями
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}  


# Админка для работы с объявлениями
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_tag', 'video_tag', 'is_premium', 'is_premium_active', 'premium_until')
    list_filter = ('is_premium', 'is_boosted', 'is_standard', 'is_popular')
    search_fields = ('title', 'description')  
    ordering = ('-created_at',)  

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" />')
        return '-'
    image_tag.short_description = "Изображение"

    def video_tag(self, obj):
        """Отображает видео в админке."""
        if obj.video:
            return mark_safe(f'<video width="100" controls><source src="{obj.video.url}" type="video/mp4">Ваш браузер не поддерживает видео.</video>')
        return 'Нет видео'
    video_tag.short_description = "Видео"

    def is_premium_active(self, obj):
        """Проверка, активен ли статус премиум."""
        return obj.is_premium_active
    is_premium_active.short_description = 'Премиум активен'


# Регистрация моделей в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)