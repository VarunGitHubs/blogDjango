# Generated by Django 4.1 on 2023-02-08 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0013_alter_post_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number_likes',
            field=models.IntegerField(default=0),
        ),
    ]
