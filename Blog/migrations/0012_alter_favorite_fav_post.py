# Generated by Django 4.0.3 on 2022-06-08 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0011_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='fav_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fav_post', to='Blog.post'),
        ),
    ]