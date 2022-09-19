from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

from .models import CustomUser


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    users = CustomUser.objects.all()
    registered_user = users[len(users)-1].email

# from urllib import request
# from django.contrib import auth
# auth.get_user(request).username
# auth.get_user(request).check_password()

    """ ВАРИАНТ-1. В этом варианте все адреса получателей будут видны всем получателям одновременно"""

    send_mail(
        subject='SENDING OPTION-1',
        message=f'Вы зарегистрировались на MMORPG сайтe. { registered_user }',
        from_email='gaidysheff@yandex.ru',
        recipient_list=['gaidysheff@mail.ru', 'gaidysheff@gmail.com', ]
    )

    """ ВАРИАНТ-2. В этом варианте адресат будет видеть только свой адрес в графе 'кому'."""

    Subject = 'SENDING OPTION-2'
    Message = f'Добро пожаловать на MMORPG сайт. Вы зарегистрировались как: { registered_user } '

    datatuple = (
        (Subject, Message, 'gaidysheff@yandex.ru',
         ['gaidysheff@mail.ru']),
        (Subject, Message, 'gaidysheff@yandex.ru',
         ['gaidysheff@gmail.com']),
    )
    send_mass_mail(datatuple)
