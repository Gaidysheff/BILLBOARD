from django.contrib import admin
from .models import Join


@admin.register(Join)
class JoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',  'timestamp',)
