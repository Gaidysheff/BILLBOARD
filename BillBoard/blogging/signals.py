from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Feedback, Post

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

        msg = EmailMultiAlternatives(
            subject=f'New post',
            from_email='gaidysheff@yandex.ru',
            to=[user.email, 'gaidysheff@mail.ru']
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


#     if created:
#         subject = f'Опубликован новый пост "{instance.post.title}" {instance.date.strftime("%d %m %Y")}'
#     else:
#         subject = f'Пост "{instance.post.title}" изменён {instance.date.strftime("%d %m %Y")}'
#     mail_managers(
#         subject=subject,
#         message=instance.message,
#     )
