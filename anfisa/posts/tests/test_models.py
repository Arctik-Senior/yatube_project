from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Текстовый пост',
            author=cls.user,
            group=cls.group
        )

    def test_models_have_correct_object_names(self):
        """Проверяем корректность отображения __str__ моделей."""
        post = self.post
        group = self.group

        # Проверка для поста
        expected_post_str = post.text[:15]
        self.assertEqual(
            str(post), expected_post_str,
            f'Метод __str__ модели Post должен возвращать {expected_post_str}'
        )

        expected_group_str = group.title
        self.assertEqual(
            str(group), expected_group_str,
            f'Метод __str__ модели Group должен возвращать {expected_group_str}'  # noqa: E501
        )

    def test_verbose_name(self):
        post = self.post

        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор поста',
            'group': 'Группа',
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text(self):
        post = self.post

        field_help_text = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }

        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
