from django.contrib import admin
from .models import Ad, Category

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_url')  # Здесь можно добавить метод для отображения изображения

admin.site.register(Ad, AdAdmin)
admin.site.register(Category)