# Generated by Django 4.0.3 on 2022-06-09 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0014_alter_favorite_user'),
        ('account', '0006_alter_userprofilepic_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilepic',
            name='post_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.post'),
        ),
    ]
