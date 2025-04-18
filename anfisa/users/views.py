# users/views.py
# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class LogoutView(DjangoLoginView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/logged_out.html'


class LoginView(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/login.html'
