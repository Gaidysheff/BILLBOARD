from django.contrib import admin

from .models import Feedback, Post


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'text', 'photo', 'upload', 'dateCreation',
                    'категория', 'автор'
                    )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    # list_editable = ('category', ) """ пригодится, когда категория будет самостоятельной моделью"""
    list_filter = (
        'dateCreation',
        # 'сategory'
    )
    prepopulated_fields = {'slug': ('title',)}

    inlines = [FeedbackInline]

    @admin.display(ordering='author')
    def автор(self, obj):
        return obj.author

    @admin.display(ordering='-category')
    def категория(self, obj):
        return obj.category


# _______добавление команд в список действий в админке ____________

    # actions = ['make_published', 'make_withdrawn']

    # @admin.action(description='Опубликовать выбранные посты')
    # def make_published(self, request, queryset):
    #     updated = queryset.update(status='p')
    #     self.message_user(request, ngettext(
    #         '%d публикация была отмечена как "Опубликованная".',
    #         '%d публикации были отмечены как "Опубликованные".',
    #         updated,
    #     ) % updated, messages.SUCCESS)

    # @admin.action(description='Отправить выбранные посты в архив')
    # def make_withdrawn(self, request, queryset):
    #     updated = queryset.update(status='w')
    #     self.message_user(request, ngettext(
    #         '%d публикация была отправлена в архив.',
    #         '%d публикации были отправлены в архив.',
    #         updated,
    #     ) % updated, messages.SUCCESS)

# -----------------------------------------------------------------
