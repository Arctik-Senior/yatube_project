from django import forms
from .models import Post  # Импортируем модель Create


class CreateForm(forms.ModelForm):
    class Meta:
        model = Post  # Указываем модель, с которой связана форма
        fields = ('text', 'group')  # Указываем поля, которые будут в форме
