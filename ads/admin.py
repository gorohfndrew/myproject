from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ad, Category
from django.utils.safestring import mark_safe  # Добавьте импорт mark_safe

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_url', 'delete_button' ,'video_preview')

    # Отображение изображения
    def image_url(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100px" />', obj.image.url)
        return '-'
    
    image_url.short_description = 'Image'
    def video_preview(self, obj):
        if obj.video:
            return mark_safe(f'<video width="150" controls><source src="{obj.video.url}" type="video/mp4"></video>')
        return '-'

    # Кнопка удаления объявления
    def delete_button(self, obj):
        # Генерируем кнопку с ссылкой на удаление
        return format_html(
            '<a class="button" href="{0}">Удалить</a>',
            reverse('admin:ads_ad_delete', args=[obj.pk])
        )
    delete_button.short_description = 'Удалить'

    video_preview.short_description = "Видео"


# Регистрация модели и админского интерфейса
admin.site.register(Category)
