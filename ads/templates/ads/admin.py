from django.contrib import admin
from django.utils.safestring import mark_safe
from ...models import Ad, Category

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'image_url')

    def image_url(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" />')
        return '-'

    image_url.short_description = 'Image'  # Заголовок для столбца

admin.site.register(Ad, AdAdmin)
admin.site.register(Category)

