# Generated by Django 4.0.3 on 2022-06-10 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_userprofilepic_foreign_key_to_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofilepic',
            name='foreign_key_to_post',
        ),
    ]