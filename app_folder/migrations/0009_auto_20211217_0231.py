# Generated by Django 2.2 on 2021-12-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_folder', '0008_auto_20211217_0218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritequote',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='favoritequote',
            name='liked_by',
            field=models.ManyToManyField(null=True, related_name='liked_quotes', to='app_folder.User'),
        ),
    ]