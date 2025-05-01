from django.urls import reverse

CREATE_POST_URL = reverse('posts:create_post')


def get_edit_post_url(post_id):
    return reverse('posts:post_edit', kwargs={'post_id': post_id})
