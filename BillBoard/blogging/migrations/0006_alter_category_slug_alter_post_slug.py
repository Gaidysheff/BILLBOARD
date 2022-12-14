# Generated by Django 4.1.1 on 2022-09-21 10:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0005_alter_category_slug_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, help_text='slug назначится автоматически', max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
