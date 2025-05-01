from django.test import Client, TestCase
from django.urls import reverse
import tempfile
import shutil
from django.conf import settings
from posts.models import Post, User, Group, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
from .constants import CREATE_POST_URL, get_edit_post_url


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='test-author-user')
        cls.group = Group.objects.create(
            title="test-title",
            slug="test-slug",
            description="test-description",
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='test-post',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='test-user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

        self.edit_form_data = {'text': 'test-edit-text'}
        self.edit_url = get_edit_post_url(self.post.id)

    def test_guest_cant_create_post(self):
        posts_count = Post.objects.count()
        form_data = {'text': 'test-new-text'}

        response = self.guest_client.post(
            CREATE_POST_URL,
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(response.status_code, 200)

    def test_auth_can_create_post(self):
        posts_count = Post.objects.count()
        form_data = {'text': 'test-new-text'}

        response = self.authorized_client.post(
            CREATE_POST_URL,
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(response.status_code, 200)

    def test_guest_cant_edit_post(self):
        response = self.guest_client.post(
            self.edit_url,
            data=self.edit_form_data,
            follow=True
        )
        self.assertNotEqual(
            Post.objects.get(pk=self.post.id).text,
            self.edit_form_data['text']
        )
        self.assertEqual(response.status_code, 200)

    def test_auth_user_cant_edit_post(self):
        response = self.authorized_client.post(
            self.edit_url,
            data=self.edit_form_data,
            follow=True
        )
        self.assertNotEqual(
            Post.objects.get(pk=self.post.id).text,
            self.edit_form_data['text']
        )
        self.assertEqual(response.status_code, 200)

    def test_author_can_edit_post(self):
        response = self.author_client.post(
            self.edit_url,
            data=self.edit_form_data,
            follow=True
        )
        self.assertEqual(
            Post.objects.get(pk=self.post.id).text,
            self.edit_form_data['text']
        )
        self.assertEqual(response.status_code, 200)


class PostImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост с картинкой',
            group=cls.group,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_image_in_context_index(self):
        response = self.authorized_client.get(reverse('posts:index'))
        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.image, self.post.image)

    def test_image_in_context_profile(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.image, self.post.image)

    def test_image_in_context_group(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.image, self.post.image)

    def test_image_in_context_post_detail(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        post = response.context['post']
        self.assertEqual(post.image, self.post.image)


class TestComment(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='test-user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.author = User.objects.create_user(username='post-author')
        self.author_client = Client()
        self.author_client.force_login(self.author)

        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )

        self.post = Post.objects.create(
            author=self.author,
            text='Тестовый пост',
            group=self.group,
        )

        self.add_comment_url = reverse('posts:add_comment', kwargs={'post_id': self.post.id})  # noqa: E501
        self.comment_data = {'text': 'test_text'}

    def test_guest_cannot_create_comment(self):
        response = self.client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            {'text': 'Test Comment'}
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post.id}/comment/'
            )

    def test_authorized_user_can_create_comment(self):
        """Авторизованный пользователь может создать комментарий."""
        response = self.authorized_client.post(
            self.add_comment_url,
            data=self.comment_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        new_comment = Comment.objects.first()
        self.assertEqual(new_comment.text, self.comment_data['text'])
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.post, self.post)
