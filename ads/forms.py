from django import forms
from .models import Ad, Category, CustomUser, Profile
from django.core.exceptions import ValidationError
from .models import CustomUser
from .widgets import MultipleFileInput


class RegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label="Номер телефону",
        widget=forms.TextInput(attrs={'placeholder': '+380', 'value': '+380'})
    )
    
    password1 = forms.CharField(
        label="Пороль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    
    password2 = forms.CharField(
        label="Підтвердження пороля",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith('+380'):
            raise ValidationError('Номер телефону повинен починатися з +380.')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не співпадають.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Хешуємо пароль
        user.phone_number = self.cleaned_data["phone_number"]  # Зберігаємо номер у користувача

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

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if data is None:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        result = []
        for file in data:
            super().clean(file, initial)
            result.append(file)
        return result

class AdForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        label="Изображения",
        help_text="Максимум 10 файлов"
    )
    city = forms.CharField(
        label="Город",
        widget=forms.TextInput(attrs={'placeholder': 'Например: Киев'}),
        required=False
    )
    class Meta:
        model = Ad
        fields = ['category', 'title', 'description', 'price', 'video', 'is_premium', 'premium_until', 'is_standard', 'is_popular', 'is_boosted','city']
        widgets = {
            'premium_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.TextInput(attrs={'placeholder': 'Договірна'})
        }

    def clean_images(self):
        images = self.cleaned_data.get('images', [])
        if len(images) > 10:
            raise ValidationError("Можно загрузить не более 10 изображений.")
        return images

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.content_type.startswith('video/'):
                raise ValidationError("Файл должен быть видео")
            if video.size > 100 * 1024 * 1024:  # 100MB
                raise ValidationError("Максимальный размер видео - 100MB")
        return video

    def clean_price(self):
        price = self.cleaned_data.get('price', '').strip()
        if not price or price == "Договірна":
            return "Договірна"
        try:
            price_value = float(price.replace(',', '.'))
            if price_value <= 0:
                raise ValidationError("Цена должна быть положительной")
            return str(price_value)
        except ValueError:
            raise ValidationError("Введите корректное число")