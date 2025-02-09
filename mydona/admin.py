from django.contrib import admin
from .models import Ad, Category
from django.utils.html import format_html

# Настройки для модели Ad
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'created_at', 'video_preview')  # Добавили 'video_preview'
    search_fields = ('title', 'description')  # Возможность поиска по этим полям
    list_filter = ('created_at',)  # Фильтрация по дате создания
    ordering = ('-created_at',)  # Сортировка по дате (новые сверху)

    def video_preview(self, obj):
        if obj.video:  # Проверяем, есть ли видео
            return format_html(
                f'<video width="100" controls><source src="{obj.video.url}" type="video/mp4"></video>'
            )
        return "Нет видео"

    video_preview.short_description = "Видео"

# Настройки для модели Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Показываем только имя категории
    search_fields = ('name',)  # Возможность поиска по имени категории

# Регистрируем модели и их классы в админке
