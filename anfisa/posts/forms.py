from django import forms
from .models import Create  # Импортируем модель Create


class CreateForm(forms.ModelForm):
    class Meta:
        model = Create  # Указываем модель, с которой связана форма
        fields = ('text', 'group')  # Указываем поля, которые будут в форме
