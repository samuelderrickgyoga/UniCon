# Generated by Django 5.0.6 on 2024-05-30 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_comment_no_of_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='no_of_likes',
        ),
        migrations.AddField(
            model_name='post',
            name='no_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
