# Generated by Django 2.1.1 on 2018-10-15 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0008_photos_mini_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='channel',
        ),
    ]
