from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Опубликован новый пост "{instance.post.title}" {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Пост "{instance.post.title}" изменён {instance.date.strftime("%d %m %Y")}'
    mail_managers(
        subject=subject,
        message=instance.message,
    )
