from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Feedback, Post


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        html = render_to_string(
            'blogging/mail.html',
            {
                'user': user,
                'comment': instance,
            },
        )

        _post = Post.objects.all()
        post = _post[len(_post)-1]

        msg = EmailMultiAlternatives(
            subject=f'Новая статья от автора { post.author } из категории { post.cat }',
            from_email='gaidysheff@yandex.ru',
            to=['gaidysheff@mail.ru', user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
