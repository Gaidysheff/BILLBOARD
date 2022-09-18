from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    """ ВАРИАНТ-1. В этом варианте все адреса получателей будут видны всем получателям одновременно"""

    send_mail(
        subject='OPTION-1',
        message='ПРОВЕРКА СОХРАНЯЕМОСТИ В ФАЙЛ. SUBJECT - НЕЧИТАЕМЫЙ',
        from_email='gaidysheff@yandex.ru',
        recipient_list=['gaidysheff@mail.ru', 'gaidysheff@gmail.com', ]
    )

    """ ВАРИАНТ-2. В этом варианте адресат будет видеть только свой адрес в графе 'кому'."""

    Subject = 'OPTION-2'
    Message = 'ПРОВЕРКА СОХРАНЯЕМОСТИ В ФАЙЛ. SUBJECT - НЕЧИТАЕМЫЙ'

    datatuple = (
        (Subject, Message, 'gaidysheff@yandex.ru',
         ['gaidysheff@mail.ru']),
        (Subject, Message, 'gaidysheff@yandex.ru',
         ['gaidysheff@gmail.com']),
    )
    send_mass_mail(datatuple)
