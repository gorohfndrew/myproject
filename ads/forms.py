from django import forms
from .models import Ad, Category, CustomUser, Profile
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label="Номер телефону",
        widget=forms.TextInput(attrs={'placeholder': '+380', 'value': '+380'})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith('+380'):
            raise ValidationError('Номер телефону повинен починатися з +380.')
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Хешируем пароль
        user.phone_number = self.cleaned_data["phone_number"]  # Сохраняем номер в пользователя

        if commit:
            user.save()
        return user
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }    
class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Здесь подтягиваются все категории из базы данных
        empty_label="Выберите категорию"   # Это текст, который будет отображаться до выбора категории
    )

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'description', 'price', 'image', 'video', 'is_premium', 'premium_until', 'is_standard', 'is_popular', 'is_boosted']
        widgets = {
            'premium_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'price': forms.TextInput(attrs={'value': 'Договореная'})  # ✅ Значение по умолчанию
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price == "Договірна":
            return "Договірна"  # ✅ Возвращаем строку, а не None

        try:
            price = float(price)  # ✅ Преобразуем в число
            if price <= 0:
                raise forms.ValidationError("Цена должна быть больше нуля.")
            return str(price)  # ✅ Возвращаем строку, так как price — CharField
        except (ValueError, TypeError):
            raise forms.ValidationError("Введите число или оставьте 'Договореная'.")
    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.name.endswith('.mp4'):
                raise forms.ValidationError("Разрешен только формат MP4 для видео.")
        return video