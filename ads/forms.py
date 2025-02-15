from django import forms
from .models import Ad
from .models import Category



class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Здесь подтягиваются все категории из базы данных
        empty_label="Выберите категорию"   # Это текст, который будет отображаться до выбора категории
    )

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'description', 'price', 'image', 'video', 'is_premium', 'premium_until','is_standard', 'is_popular', 'is_boosted']
        widgets = {
            'premium_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля.")
        return price

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.name.endswith('.mp4'):
                raise forms.ValidationError("Разрешен только формат MP4 для видео.")
        return video