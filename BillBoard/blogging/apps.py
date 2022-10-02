from django.apps import AppConfig


class BloggingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogging'
    verbose_name = 'MMORPG - Доска объявлений'

    def ready(self):
        import blogging.signals
