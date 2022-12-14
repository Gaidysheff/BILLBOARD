from django.db import models


class Join(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['email', ]

    def __str__(self):
        return self.email
