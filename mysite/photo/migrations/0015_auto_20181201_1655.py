# Generated by Django 2.1.1 on 2018-12-01 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0014_mini_nuser_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mini_poetry',
            name='dubbing',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mini_poetry',
            name='dubbing_1',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mini_poetry',
            name='dubbing_2',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
