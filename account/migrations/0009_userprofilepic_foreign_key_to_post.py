# Generated by Django 4.0.3 on 2022-06-10 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0018_remove_comment_email_remove_comment_name'),
        ('account', '0008_remove_userprofilepic_post_related'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilepic',
            name='foreign_key_to_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.post'),
        ),
    ]