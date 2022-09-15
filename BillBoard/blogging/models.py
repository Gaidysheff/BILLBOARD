from django.db import models
from django.utils.translation import gettext_lazy as _

from customuser.models import CustomUser


class Post(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guildmasters', 'Гильдмастера'),
        ('questgivers', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, unique=False)
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='URL', help_text=_('slug назначится автоматически'))
    text = models.TextField(verbose_name='Текст поста',
                            help_text=_('Введите здесь текст своего Поста.'))
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name='Изображение')
    upload = models.FileField(upload_to='uploads/')
    category = models.CharField(max_length=64, choices=TYPE, default='tanks')
    dateCreation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title


class Feedback(models.Model):
    author = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:10]}...'
