from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.core.mail import send_mail

def index(request):
    posts = Post.objects.all()

    send_mail(
        subject='Подписка на рассылку',
        message='Вы подписались на рассылку новостей в выбранной категории',
        from_email='gaidysheff@yandex.ru',
        recipient_list=['gaidysheff@mail.ru', ]
        )

    return render(request, 'blogging/HomePage.html', {'posts': posts, 'title': 'Главная страница'})


def category(request, type):
    return HttpResponse(f"<h1>Объявы по категориям</h1><p>{type}</p>")


def login(request):
    return HttpResponse("<h1>Авторизация</h1>")


def about(request):
    return render(request, 'blogging/about.html', {'title': 'О сайте'})


def contact(request):
    return HttpResponse("<h1>Контакты</h1>")


def pageNotFound(request, exception):
    return render(request, 'blogging/PageNotFound.html')






