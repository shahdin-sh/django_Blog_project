# Generated by Django 4.0.3 on 2022-06-09 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0017_alter_comment_email_alter_comment_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]