# Generated by Django 4.0.3 on 2022-07-04 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0043_comment_user_likes_delete_favoritecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='datetime_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
