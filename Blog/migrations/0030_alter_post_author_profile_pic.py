# Generated by Django 4.0.3 on 2022-06-13 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_userprofilepic_profile_pic'),
        ('Blog', '0029_alter_post_author_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author_profile_pic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='account.userprofilepic'),
        ),
    ]