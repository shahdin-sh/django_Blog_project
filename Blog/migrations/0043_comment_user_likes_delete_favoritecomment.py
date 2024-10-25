# Generated by Django 4.0.3 on 2022-07-04 06:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0042_favoritecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FavoriteComment',
        ),
    ]
