from django import forms
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['multiple'] = 'multiple'  # Добавляем атрибут multiple
        return super().render(name, value, attrs, renderer)