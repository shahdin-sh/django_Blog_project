# Generated by Django 4.0.3 on 2022-06-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_userprofilepic_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilepic',
            name='profile_pic',
            field=models.ImageField(default='default_profile_pic/img_avatar.png', upload_to='profile/'),
        ),
    ]
