from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'blogging/HomePage.html', {'title': 'Главная страница'})


def category(request, type):
    return HttpResponse(f"<h1>Объявы по категориям</h1><p>{type}</p>")


def login(request):
    return HttpResponse("<h1>Авторизация</h1>")


def about(request):
    return HttpResponse("<h1>О нас</h1>")


def contact(request):
    return HttpResponse("<h1>Контакты</h1>")


def pageNotFound(request, exception):
    return render(request, 'blogging/PageNotFound.html')
