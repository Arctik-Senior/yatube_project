# from django.http import HttpResponse
from django.shortcuts import render

from .models import Post
# Create your views here.


def index(request):
    template = 'posts/index.html'
    text = 'Это главная страница проекта Yatube'
    posts = Post.objects.all()

    context = {
        'text': text,
        'posts': posts
    }
    return render(request, template, context)


def group_list(request):
    template = 'posts/group_list.html'
    textt = 'Здесь будет информация о группах проекта Yatube'

    context = {
        'textt': textt
    }
    return render(request, template, context)
