# Generated by Django 4.0.3 on 2022-06-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userprofilepic_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilepic',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile/'),
        ),
    ]