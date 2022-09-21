from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from customuser.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='Заголовок поста')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='URL', help_text=_('slug назначится автоматически'))
    text = models.TextField(verbose_name='Текст поста',
                            help_text=_('Введите здесь текст своего Поста.'))
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name='Изображение')
    upload = models.FileField(upload_to='uploads/', verbose_name='Видео файлы')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория поста')
    dateCreation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-dateCreation', 'title']

    def __str__(self):
        return f'{self.title[:10]}...'

    def preview(self):
        return '{} ... {}'.format(self.text[0:123], str(self.rating))

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # TYPE = (
    #     ('tanks', 'Танки'),
    #     ('healers', 'Хилы'),
    #     ('dd', 'ДД'),
    #     ('traders', 'Торговцы'),
    #     ('guildmasters', 'Гильдмастера'),
    #     ('questgivers', 'Квестгиверы'),
    #     ('smith', 'Кузнецы'),
    #     ('tanners', 'Кожевники'),
    #     ('potionmakers', 'Зельевары'),
    #     ('spellmasters', 'Мастера заклинаний'),
    # )


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('category', kwargs={'сategory_slug': self.slug})
        return reverse('category', kwargs={'cat_id': self.pk})
        # для обычного РК


class Feedback(models.Model):
    author = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Пост')
    status = models.BooleanField(default=False, verbose_name='Статус')
    dateCreation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.text[:10]}...'
