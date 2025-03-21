# from django.http import HttpResponse
from .models import Post, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import CreateForm
# Create your views here.


def index(request):
    template = 'posts/index.html'
    text = 'Это главная страница проекта Yatube'
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядеть так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 5)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # posts = Post.objects.all()

    context = {
        'text': text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_list(request, username):
    template = 'posts/group_list.html'
    textt = 'Здесь будет информация о группах проекта Yatube'
    context = {
        'textt': textt,
    }
    return render(request, template, context)


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


def post_create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Устанавливаем автора поста
            post.save()
            return redirect('profile', username=request.user.username)
        # Редирект на профиль
    else:
        form = CreateForm()

    return render(request, 'posts/create_post.html', {'form': form})
