# from django.http import HttpResponse
from .models import Post, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PostForm
# Create your views here.

POSTS_PER_PAGE = 10
LEN_SHORT_POST = 30
LENGTH = 10


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, LENGTH)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "title": "Последние обновления на сайте",
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    # Передаем модель Group как первый аргумент
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()  # Через related_name
    context = {
        'author': user,
        'posts': posts,
        'post_count': posts.count(),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author', 'group'),
                             id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    user = request.user
    form = PostForm(request.POST or None)

    if form.is_valid():

        post = form.save(commit=False)
        post.author = user
        post.save()

        return redirect('posts:profile', user.username)

    context = {
        'form': form,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect(f'/posts/{post_id}')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():

            form.save()

            return redirect(f'/posts/{post_id}')

    form = PostForm(
        initial={
            'text': post.text,
            'group': post.group,
        }
    )
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)
