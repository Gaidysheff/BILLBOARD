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
    # cats = Category.objects.all()

    context = {
        'menu': menu,
        'posts': posts,
        # 'cats': cats,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'blogging/HomePage.html', context=context)


def show_post(request, post_id):
    return HttpResponse(f"<h1>Отображение статьи с id = {post_id}</h1>")


def show_category(request, cat_id):
    posts = Post.objects.filter(category=cat_id)
    cats = Category.objects.all()
    context = {
        'menu': menu,
        'posts': posts,
        'cats': cats,
        'title': 'Отображение по категориям',
        'cat_selected': cat_id,
    }
    return render(request, 'blogging/HomePage.html', context=context)


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
