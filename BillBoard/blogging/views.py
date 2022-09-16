from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.core.mail import send_mail, send_mass_mail


def index(request):
    posts = Post.objects.all()

    """ ВАРИАНТ-1. В этом варианте все адреса получателей будут видны всем получателям одновременно"""

    # send_mail(
    #     subject='Подписка на рассылку. В ПИСЬМЕ ЧИТАЕМО, В ФАЙЛЕ - НЕЧИТАЕМО',
    #     message='ПРОВЕРКА СОХРАНЯЕМОСТИ В ФАЙЛ. SUBJECT - НЕЧИТАЕМЫЙ',
    #     from_email='gaidysheff@yandex.ru',
    #     recipient_list=['gaidysheff@mail.ru', 'gaidysheff@gmail.com', ]
    # )

    """ ВАРИАНТ-2. В этом варианте адресат будет видеть только свой адрес в графе 'кому'."""

    Subject = 'Подписка на рассылку. В ПИСЬМЕ ЧИТАЕМО, В ФАЙЛЕ - НЕЧИТАЕМО'
    Message = 'ПРОВЕРКА СОХРАНЯЕМОСТИ В ФАЙЛ. SUBJECT - НЕЧИТАЕМЫЙ'

    datatuple = (
        (Subject, Message, 'gaidysheff@yandex.ru',
         ['gaidysheff@mail.ru']),
        (Subject, Message, 'gaidysheff@yandex.ru',
         ['gaidysheff@gmail.com']),
    )
    send_mass_mail(datatuple)

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
