# Generated by Django 4.1.1 on 2022-09-21 11:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0011_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, help_text='slug назначится автоматически', max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
