# Generated by Django 4.0.2 on 2022-03-27 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_post_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="user",
        ),
    ]