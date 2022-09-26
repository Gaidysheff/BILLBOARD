from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic

from .forms import CustomUserCreationForm
from .models import CustomUser
from .token import account_activation_token

# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'

#     users = CustomUser.objects.all()
#     registered_user = users[len(users)-1].email


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# --------------------------------------------------------------------------

    # """ ВАРИАНТ-1. В этом варианте все адреса получателей будут видны всем получателям одновременно"""

    # send_mail(
    #     subject='SENDING OPTION-1',
    #     message=f'Вы зарегистрировались на MMORPG сайтe. { registered_user }',
    #     from_email='gaidysheff@yandex.ru',
    #     recipient_list=['gaidysheff@mail.ru', 'gaidysheff@gmail.com', ]
    # )

    # """ ВАРИАНТ-2. В этом варианте адресат будет видеть только свой адрес в графе 'кому'."""

    # Subject = 'SENDING OPTION-2'
    # Message = f'Добро пожаловать на MMORPG сайт. Вы зарегистрировались как: { registered_user } '

    # datatuple = (
    #     (Subject, Message, 'gaidysheff@yandex.ru',
    #      ['gaidysheff@mail.ru']),
    #     (Subject, Message, 'gaidysheff@yandex.ru',
    #      ['gaidysheff@gmail.com']),
    # )
    # send_mass_mail(datatuple)
