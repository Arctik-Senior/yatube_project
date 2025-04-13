from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Group(models.Model):
    title = models.TextField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Адрес группы')
    description = models.TextField(verbose_name='описание группы')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(null=True,
                            verbose_name="Текст поста",
                            help_text='Введите текст поста')

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор поста",
    )

    group = models.ForeignKey(
        Group,
        verbose_name="Группа",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        help_text='Группа, к которой будет относиться пост'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class Create(models.Model):
    text = models.TextField(verbose_name='Текст поста',
                            null=False, blank=False)
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='create_posts',
        verbose_name="Группа"
    )

    def __str__(self):
        return self.text
