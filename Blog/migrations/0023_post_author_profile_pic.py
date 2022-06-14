# Generated by Django 4.0.3 on 2022-06-13 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_userprofilepic_profile_pic'),
        ('Blog', '0022_remove_post_author_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_profile_pic',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.userprofilepic'),
        ),
    ]
