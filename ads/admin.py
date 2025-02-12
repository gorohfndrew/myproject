from django.contrib import admin
from django.utils.html import format_html
from .models import Ad, Category

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_premium', 'created_at', 'image_url', 'video_preview','is_standard', 'is_popular', 'is_boosted')
    list_filter = ('is_premium',)

    # Отображение изображения
    def image_url(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100px" />', obj.image.url)
        return '-'
    
    image_url.short_description = 'Image'
    
    # Превью видео
    def video_preview(self, obj):
        if obj.video:
            return format_html(f'<video width="150" controls><source src="{obj.video.url}" type="video/mp4"></video>')
        return '-'

    video_preview.short_description = "Видео"

# Регистрируем модель Ad в админке
admin.site.register(Ad, AdAdmin)  # Оставляем здесь!
admin.site.register(Category)