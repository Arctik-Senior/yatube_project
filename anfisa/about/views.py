from django.views.generic.base import TemplateView
# Create your views here.


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_title'] = 'Очень простая страница'
        context['just_text'] = ('На создание этой страницы '
                                'у меня ушло пять минут! Ай да я.')
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_title'] = 'Очень простая страница'
        context['just_text'] = ('На создание этой страницы '
                                'у меня ушло пять минут! Ай да я.')
        return context
