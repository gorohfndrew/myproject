from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'description', 'price', 'image', 'video', 'is_premium', 'premium_until']  # Добавьте 'is_premium' и 'premium_until'
        widgets = {
            'premium_until': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }