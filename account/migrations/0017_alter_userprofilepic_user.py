# Generated by Django 4.0.3 on 2022-06-14 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0016_alter_userprofilepic_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilepic',
            name='user',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
