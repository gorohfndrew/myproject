from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ad, Category

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_url', 'delete_button')

    # Отображение изображения
    def image_url(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100px" />', obj.image.url)
        return '-'
    
    image_url.short_description = 'Image'

    # Кнопка удаления объявления
    def delete_button(self, obj):
        # Генерируем кнопку с ссылкой на удаление
        return format_html(
            '<a class="button" href="{0}">Удалить</a>',
            reverse('admin:ads_ad_delete', args=[obj.pk])
        )
    delete_button.short_description = 'Удалить'

# Регистрация модели и админского интерфейса
admin.site.register(Category)
