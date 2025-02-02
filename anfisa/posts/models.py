from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name="Текст поста")
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name="Дата публикации")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name="Группа"
    )

    def __str__(self):
        return self.text[:15]  # Возвращает первые 15 символов текста


class Group(models.Model):
    title = models.TextField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Адрес группы')
    description = models.TextField(verbose_name='описание группы')

    def __str__(self):
        return self.title
