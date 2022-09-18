from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить блог", 'url_name': 'add_blog'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


def index(request):
    posts = Post.objects.all()
    context = {
        'menu': menu,
        'posts': posts,
        'title': 'Главная страница'
    }
    return render(request, 'blogging/HomePage.html', context=context)


def category(request, type):
    return HttpResponse(f"<h1>Объявы по категориям</h1><p>{type}</p>")


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'blogging/login.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))


def addblog(request):
    return HttpResponse("Добавление статьи")


def about(request):
    return render(request, 'blogging/about.html', {'title': 'О сайте'})


def contact(request):
    return HttpResponse("<h1>Контакты</h1>")


def pageNotFound(request, exception):
    return render(request, 'blogging/PageNotFound.html')
