# Generated by Django 4.0.3 on 2022-06-14 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_userprofilepic_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofilepic',
            old_name='user',
            new_name='author',
        ),
    ]