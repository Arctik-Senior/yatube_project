from django import forms
from .models import Post  # Импортируем модель Create
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': _('Текст поста'),
            'group': _('Вы можете указать группу к посту')
        }
