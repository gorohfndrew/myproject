from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Ad, Category
from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")  # Показываем номер в админке
    search_fields = ("user__username", "phone_number")

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Дополнительная информация"

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)  # Встраиваем профиль в UserAdmin
    list_display = ('username', 'email', 'get_phone_number', 'is_staff')

    def get_phone_number(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else "Нет номера"
    get_phone_number.short_description = "Номер телефона"




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