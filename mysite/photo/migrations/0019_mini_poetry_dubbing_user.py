# Generated by Django 2.1.1 on 2018-12-04 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0018_auto_20181201_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='mini_poetry',
            name='dubbing_user',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
