# Generated by Django 4.0.3 on 2022-06-09 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_userprofilepic_post_related'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofilepic',
            name='post_related',
        ),
    ]
