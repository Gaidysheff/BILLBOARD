from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Category, Feedback, Post


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'post', 'status', 'dateCreation',)
    search_fields = ('author', )
    list_filter = ('status', 'dateCreation', )
    list_editable = ('status', 'author',)

# _______добавление команд в список действий в админке ____________

    actions = ['make_published', 'make_withdrawn']

    @admin.action(description='Опубликовать выбранные комментарии')
    def make_published(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, ngettext(
            '%d комментарий был отмечен как "Опубликован".',
            '%d комментарии были отмечены как "Опубликованные".',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Отправить выбранные комментарии в архив')
    def make_withdrawn(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, ngettext(
            '%d комментарий был отправлен в черновик.',
            '%d комментарии были отправлены в черновик.',
            updated,
        ) % updated, messages.SUCCESS)

# -----------------------------------------------------------------


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'text', 'photo',
                    'upload', 'dateCreation', 'cat', 'author', )
    list_display_links = ('id', 'title', )
    search_fields = ('title', 'text', )
    list_editable = ('cat', 'author',)
    list_filter = ('dateCreation', )
    prepopulated_fields = {'slug': ('title',)}

    inlines = [FeedbackInline]

    # @admin.display(ordering='author')
    # def автор(self, obj):
    #     return obj.author

    # @admin.display(ordering='-category')
    # def категория(self, obj):
    #     return obj.category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', )
    search_fields = ('name', )
    list_filter = ('name', )
    prepopulated_fields = {'slug': ('name',)}
