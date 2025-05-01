from django import forms
from .models import Post, Comment  # Импортируем модель Create
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': _('Текст поста'),
            'group': _('Вы можете указать группу к посту'),
            'image': _('Вы можете добавить картинку')
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
            }),
        }
        help_texts = {
            'text': _('Текст комментария')
        }
