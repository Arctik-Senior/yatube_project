# from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Post, Group, Follow
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
        """URL использует соответствующий шаблон."""
        templates_pages_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }

        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
            self.assertTemplateUsed(response, template)


'''
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
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache(self):
        # Первый запрос (кешируем)
        response1 = self.authorized_client.get(reverse('posts:index'))
        content1 = response1.content

        # Создаем новый пост
        Post.objects.create(
            text="new-post-text",
            author=self.user
        )

        # Второй запрос (должен быть закеширован)
        response2 = self.authorized_client.get(reverse('posts:index'))
        content2 = response2.content

        # Проверяем, что контент не изменился (кеш работает)
        self.assertEqual(content1, content2)

        # Очищаем кеш
        cache.clear()

        # Третий запрос (должен показать новый пост)
        response3 = self.authorized_client.get(reverse('posts:index'))
        content3 = response3.content

        # Проверяем, что контент изменился после очистки кеша
        self.assertNotEqual(content1, content3)
'''

class TestFollow(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='12345')
        self.user2 = User.objects.create_user(username='test2', password='12345')
        self.client.force_login(self.user1)

    def test_follow(self):
        response = self.client.post(
            reverse('posts:profile_follow', args=[self.user2.username])
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Follow.objects.filter(user=self.user1, author=self.user2).exists()
        )

    def test_unfollow(self):
        Follow.objects.create(user=self.user1, author=self.user2)
        response = self.client.post(
            reverse('posts:profile_unfollow', args=[self.user2.username])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Follow.objects.filter(user=self.user1, author=self.user2).exists()
        )

    def test_post_in_follow_feed(self):
        Follow.objects.create(user=self.user1, author=self.user2)

        post = Post.objects.create(
            author=self.user2, text='Test post'
        )

        response = self.client.get(reverse('posts:follow_index'))
        self.assertContains(response, post.text)

    def test_post_not_in_follow_feed(self):
        post = Post.objects.create(
            author=self.user2, text='Test post'
        )

        response = self.client.get(reverse('posts:follow_index'))
        self.assertNotContains(response, post.text)
