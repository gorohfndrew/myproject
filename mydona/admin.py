from django.contrib import admin
from .models import Ad, Category

# Настройки для модели Ad
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'created_at')  # Какие поля показывать в списке
    search_fields = ('title', 'description')  # Возможность поиска по этим полям
    list_filter = ('created_at',)  # Возможность фильтровать по этим полям
    ordering = ('-created_at',)  # Сортировка по полю 'created_at' (от новых к старым)

# Настройки для модели Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Показываем только имя категории
    search_fields = ('name',)  # Возможность поиска по имени категории

# Регистрируем модели и их классы в админке
admin.site.register(Ad, AdAdmin)
admin.site.register(Category, CategoryAdmin)
# Register your models here.
