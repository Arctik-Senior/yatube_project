from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Post, Group
from django.urls import reverse
from django.urls import reverse_lazy
INDEX_URL = reverse_lazy('posts:index')

User = get_user_model()


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='testuser')
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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        '''URL использует соответствующий шаблон.'''
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ),
            'posts/profile.html': reverse(
                'posts:profile',
                kwargs={'username': self.user.username}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            ),
            'posts/create_post.html': reverse('posts:create_post'),
            'posts/create_post.html': reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class CachePageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-user')
        cls.post = Post.objects.create(
            text="test-post-text",
            author=cls.user
        )

    def setUp(self):
        self.user = User.objects.get(username='test-user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache(self):
        cache.clear()
        self.authorized_client.get(reverse(INDEX_URL))

        Post.objects.create(
            text="test-post-text",
            author=self.user
        )

        new_resp = self.authorized_client.get(reverse(INDEX_URL))
        context = new_resp.context
        self.assertIsNone(context)

        cache.clear()

        new_resp = self.authorized_client.get(reverse(INDEX_URL))
        context = new_resp.context
        self.assertIsNotNone(context)
